import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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

    def on_clicked_design(*args):
        designer = filter_widget.designer

        try:
            params = designer.params
            print(params)

            dt = 1 / params['fs']

            system = designer.design(params)
            system = signal.dlti(*system, dt=dt)

            filter_view.system = system

        except Exception as e:
            show_error_dialog(e)
            raise e

    design_button.connect('clicked', on_clicked_design)

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
