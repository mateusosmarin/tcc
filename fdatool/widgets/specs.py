import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from fdatool.widgets.inputs import LabeledComboBoxText, LabeledEntry


class Specs(Gtk.VBox):
    def __init__(self, labels, parse=str):
        Gtk.VBox.__init__(self, spacing=4)
        self.parse = parse
        self.labels = labels

    @property
    def fields(self):
        return self.__labels

    @fields.setter
    def labels(self, labels):
        self.__labels = labels
        self.update_ui()

    @property
    def values(self):
        return {child.name: child.value
                for child in self.get_children()}

    def clear(self):
        for child in self.get_children():
            self.remove(child)

    def update_ui(self):
        self.clear()
        for label in self.labels:
            self.pack_start(LabeledEntry(label, parse=self.parse),
                            expand=False, fill=True, padding=0)
            self.show_all()


class FrequencySpecs(Gtk.VBox):
    def __init__(self, state, states):
        Gtk.VBox.__init__(self, spacing=4)

        self.__state = state
        self.__states = states

        self.units = LabeledComboBoxText(label='Frequencies in', options=['Hz', 'kHz', 'MHz', 'GHz'])
        self.sampling = LabeledEntry(label='Fs', parse=float)
        self.specs = Specs(states[state], parse=float)

        self.pack_start(self.units, expand=True, fill=True, padding=0)
        self.pack_start(self.sampling, expand=True, fill=True, padding=0)
        self.pack_start(self.specs, expand=True, fill=True, padding=0)

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state
        self.specs.labels = self.states[state]

    @property
    def states(self):
        return self.__states

    @states.setter
    def states(self, states):
        self.__states = states
        self.specs.labels = self.states[self.state]

    @property
    def values(self):
        unit = self.units.value
        sampling = self.sampling.value
        specs = self.specs.values
        return {'unit': unit, 'Fs': sampling, **specs}


class AmplitudeSpecs(Gtk.VBox):
    def __init__(self, state, states):
        Gtk.VBox.__init__(self, spacing=4)

        self.__state = state
        self.__states = states

        self.units = LabeledComboBoxText(label='Amplitudes in', options=['dB', 'V', 'W'])
        self.specs = Specs(states[state], parse=float)

        self.pack_start(self.units, expand=False, fill=True, padding=0)
        self.pack_start(self.specs, expand=False, fill=True, padding=0)

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state
        self.specs.labels = self.states[state]

    @property
    def states(self):
        return self.__states

    @states.setter
    def states(self, states):
        self.__states = states
        self.specs.labels = self.states[self.state]

    @property
    def values(self):
        unit = self.units.value
        specs = self.specs.values
        return {'unit': unit, **specs}


if __name__ == '__main__':
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    frequency_states = {
        'Lowpass': ['Fpass', 'Fstop'],
        'Highpass': ['Fstop', 'Fpass'],
        'Bandpass': ['Fstop1', 'Fpass1', 'Fpass2', 'Fstop2'],
        'Bandstop': ['Fpass1', 'Fstop1', 'Fstop2', 'Fpass2'],
    }

    amplitude_states = {
        'Lowpass': ['Apass', 'Astop'],
        'Highpass': ['Astop', 'Apass'],
        'Bandpass': ['Astop1', 'Apass1', 'Apass2', 'Astop2'],
        'Bandstop': ['Apass1', 'Astop1', 'Astop2', 'Apass2'],
    }

    filter_type = LabeledComboBoxText(label='Filter type', options=frequency_states.keys())
    frequency_specs = FrequencySpecs(state=filter_type.value, states=frequency_states)
    amplitude_specs = AmplitudeSpecs(state=filter_type.value, states=amplitude_states)
    button = Gtk.Button(label='Design')

    def on_clicked(*args):
        print(f'Filter type: {filter_type.value}')

        print('Frequency specifications')
        print(frequency_specs.values)

        print('Amplitude specifications')
        print(amplitude_specs.values)

    @filter_type.changed.register
    def set_state(value):
        frequency_specs.state = value
        amplitude_specs.state = value

    button.connect('clicked', on_clicked)

    box = Gtk.VBox(spacing=4, margin=4)
    hbox = Gtk.HBox(spacing=4, margin=4)
    box.pack_start(filter_type, expand=False, fill=True, padding=0)
    hbox.pack_start(frequency_specs, expand=True, fill=True, padding=0)
    hbox.pack_start(amplitude_specs, expand=True, fill=True, padding=0)
    box.pack_start(hbox, expand=True, fill=True, padding=0)
    box.pack_start(button, expand=False, fill=True, padding=0)

    window.add(box)
    window.show_all()

    Gtk.main()
