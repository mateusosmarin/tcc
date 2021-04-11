import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from fdatool.utils import amplitude_units, frequency_units
from fdatool.widgets.figures import FilterView
from fdatool.widgets.inputs import LabeledComboBoxText, LabeledEntry
from fdatool.widgets.specs import AmplitudeSpecs, FrequencySpecs

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


class Remez(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self, spacing=4)

        self.response_type = LabeledComboBoxText(label='Response type', options=frequency_states.keys())
        self.filter_order = LabeledEntry(label='Number of taps', parse=int)
        self.frequency_specs = FrequencySpecs(state=self.response_type.value, states=frequency_states)
        self.amplitude_specs = AmplitudeSpecs(state=self.response_type.value, states=amplitude_states)

        @self.response_type.changed.register
        def set_frequency_specs_state(response_type):
            self.frequency_specs.state = response_type
            self.amplitude_specs.state = response_type

        self.pack_start(self.response_type, expand=False, fill=True, padding=0)
        self.pack_start(self.filter_order, expand=False, fill=True, padding=0)
        self.pack_start(self.frequency_specs, expand=False, fill=True, padding=0)
        self.pack_start(self.amplitude_specs, expand=False, fill=True, padding=0)

    @property
    def params(self):
        numtaps = self.filter_order.value

        frequency_specs = self.frequency_specs.values
        unit = frequency_specs.pop('unit')
        scale = frequency_units[unit]
        frequency_specs = {key: scale(value)
                           for key, value in frequency_specs.items()}

        fs = frequency_specs.pop('Fs')

        amplitude_specs = self.amplitude_specs.values
        unit = amplitude_specs.pop('unit')
        scale = amplitude_units[unit]
        amplitude_specs = {key: 10 ** (scale(value) / 20)
                           for key, value in amplitude_specs.items()}

        bands = tuple(frequency_specs.values())
        bands = (0, *bands, fs / 2)

        desired = tuple(amplitude_specs.values())
        desired = (desired[0], *desired, desired[-1])[::2]

        return {
            'numtaps': numtaps,
            'bands': bands,
            'desired': desired,
            'fs': fs,
        }

    def design(self, params):
        coeffs = signal.remez(**params)

        den = np.zeros_like(coeffs)
        den[0] = 1

        return coeffs, den

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    specs_label = Gtk.Label()
    specs_label.set_markup('<b>Filter specifications</b>')

    remez = Remez()

    design_button = Gtk.Button(label='Design')

    filter_view = FilterView()

    def on_clicked_design(*args):
        params = remez.params
        print(params)

        dt = 1 / params['fs']

        system = remez.design(params)
        system = signal.dlti(*system, dt=dt)

        filter_view.system = system

    design_button.connect('clicked', on_clicked_design)

    vbox = Gtk.VBox(spacing=4, margin=4)
    vbox.pack_start(specs_label, expand=False, fill=True, padding=10)
    vbox.pack_start(remez, expand=False, fill=True, padding=0)
    vbox.pack_start(design_button, expand=False, fill=True, padding=0)

    hbox = Gtk.HBox(spacing=4, margin=4)
    hbox.pack_start(vbox, expand=False, fill=True, padding=0)
    hbox.pack_start(Gtk.VSeparator(), expand=False, fill=True, padding=4)
    hbox.pack_start(filter_view, expand=True, fill=True, padding=0)

    window.add(hbox)

    window.show_all()

    Gtk.main()
