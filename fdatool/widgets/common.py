import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from fdatool.utils import Event
from fdatool.widgets.inputs import LabeledEntry, LabeledComboBoxText


class CheckButton(Gtk.CheckButton):
    __value = False

    def __init__(self, *args, **kwargs):
        Gtk.CheckButton.__init__(self, *args, **kwargs)
        self.changed = Event()
        self.connect('toggled', self.on_toggled)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.changed.notify(value)

    def on_toggled(self, *args):
        self.value = self.get_active()


class FilterOrder(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self, spacing=4)

        self.order = LabeledEntry(label='Filter order', parse=int)
        self.order.entry.set_sensitive(False)

        self.minimum = CheckButton(label='Minimum')
        self.minimum.set_active(True)

        @self.minimum.changed.register
        def change_entry(*args):
            self.order.entry.set_text('')
            self.order.entry.set_sensitive(not self.minimum.value)

        self.pack_start(self.order, expand=True, fill=False, padding=0)
        self.pack_start(self.minimum, expand=False, fill=True, padding=0)

    @property
    def value(self):
        return self.order.value


if __name__ == '__main__':
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    filter_order = FilterOrder()

    window.add(filter_order)

    window.show_all()

    Gtk.main()
