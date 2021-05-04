import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pickle
import fdatool.filters.factory as factory
from fdatool.widgets.inputs import LabeledComboBoxText
from fdatool.widgets.figures import FilterView

from scipy import signal


class FilterWidget(Gtk.VBox):
    __state = None

    def __init__(self, state):
        Gtk.VBox.__init__(self, spacing=4)

        self.state = state

    def clear(self):
        for child in self.get_children():
            self.remove(child)

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

        self.clear()

        self.designer = factory.build(state)
        self.pack_start(self.designer, expand=True, fill=True, padding=0)

        self.show_all()


def show_error_dialog(msg):
    dialog = Gtk.MessageDialog(
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=str(msg)
    )
    dialog.run()
    dialog.destroy()


if __name__ == '__main__':
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    specs_label = Gtk.Label()
    specs_label.set_markup('<b>Filter specifications</b>')

    design_method = LabeledComboBoxText(label='Design method', options=factory.filters.keys())

    filter_widget = FilterWidget(design_method.value)

    @design_method.changed.register
    def set_filter(name):
        filter_widget.state = name

    design_button = Gtk.Button(label='Design')

    export_button = Gtk.Button(label='Export')
    export_button.show()

    def on_clicked_design(*args):
        designer = filter_widget.designer

        try:
            params = designer.params
            print(params)

            dt = 1 / params['fs']

            system = designer.design(params)
            system = signal.dlti(*system, dt=dt)

            filter_view.system = system

            if export_button not in vbox.get_children():
                vbox.pack_start(export_button, expand=False, fill=True, padding=0)

        except Exception as e:
            if export_button in vbox.get_children():
                vbox.remove(export_button)
            show_error_dialog(e)
            raise e

    design_button.connect('clicked', on_clicked_design)

    def on_export_filter(*args):
        dialog = Gtk.FileChooserDialog(
            title='Save filter',
            parent=window,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        dialog.set_current_name('untitled.pickle')

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            with open(filename, 'wb') as f:
                pickle.dump(filter_view.system, f)

        dialog.destroy()

    export_button.connect('clicked', on_export_filter)

    filter_view = FilterView()

    vbox = Gtk.VBox(spacing=4, margin=4)
    vbox.pack_start(specs_label, expand=False, fill=True, padding=10)
    vbox.pack_start(design_method, expand=False, fill=True, padding=0)
    vbox.pack_start(filter_widget, expand=True, fill=True, padding=0)
    vbox.pack_start(design_button, expand=False, fill=True, padding=0)

    hbox = Gtk.HBox(spacing=4, margin=4)

    hbox.pack_start(vbox, expand=False, fill=True, padding=0)
    hbox.pack_start(Gtk.VSeparator(), expand=False, fill=True, padding=4)
    hbox.pack_start(filter_view, expand=True, fill=True, padding=0)

    window.add(hbox)

    window.show_all()

    Gtk.main()
