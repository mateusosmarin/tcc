import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from fdatool.utils import Event


class LabeledEntry(Gtk.HBox):
    __value = ''

    def __init__(self, label, parse=str):
        Gtk.HBox.__init__(self, spacing=4)

        self.changed = Event()

        self.name = label

        self.label = Gtk.Label(label=f'{label}:')
        self.entry = Gtk.Entry()

        if parse in [int, float]:
            self.entry.set_alignment(xalign=1)
            self.entry.set_width_chars(12)
            self.entry.set_max_width_chars(12)

        self.parse = parse

        self.entry.connect('changed', self.on_changed)
        self.pack_start(self.label, expand=True, fill=True, padding=0)
        self.pack_start(self.entry, expand=False, fill=True, padding=0)

    @property
    def value(self):
        try:
            return self.parse(self.__value)
        except ValueError:
            return None

    @value.setter
    def value(self, value):
        self.__value = value
        self.entry.set_text(value)
        self.changed.notify(self.value)


    def on_changed(self, entry):
        self.value = entry.get_text()


class LabeledComboBoxText(Gtk.HBox):
    __value = None
    __options = []

    def __init__(self, label, options):
        Gtk.HBox.__init__(self, spacing=4)

        self.changed = Event()

        self.name = label

        self.label = Gtk.Label(label=f'{label}:')

        self.combo = Gtk.ComboBoxText()
        self.combo.set_entry_text_column(0)

        for option in options:
            self.combo.append_text(option)

        self.combo.set_active(0)
        self.value = self.combo.get_active_text()

        self.on_changed(self.combo)
        self.combo.connect('changed', self.on_changed)

        self.pack_start(self.label, expand=True, fill=True, padding=0)
        self.pack_start(self.combo, expand=False, fill=True, padding=0)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.changed.notify(self.value)

    def on_changed(self, combo):
        self.value = combo.get_active_text()


if __name__ == '__main__':
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    entry = LabeledEntry(label='Entry')
    numeric_entry = LabeledEntry(label='Numeric entry', parse=float)
    combo = LabeledComboBoxText(label='Combo', options=['Option 1', 'Option 2'])
    button = Gtk.Button(label='Submit')

    entry.changed.register(print)
    numeric_entry.changed.register(print)
    combo.changed.register(print)

    def on_clicked(*args):
        print({widget.name: widget.value
               for widget in (entry, numeric_entry, combo)})

    button.connect('clicked', on_clicked)

    box = Gtk.VBox()
    box.add(entry)
    box.add(numeric_entry)
    box.add(combo)
    box.add(button)

    window.add(box)
    window.show_all()
    Gtk.main()
