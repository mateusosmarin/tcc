import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from scipy import signal

from fdatool.utils import amplitude_units, frequency_units
from fdatool.widgets.common import FilterOrder
from fdatool.widgets.figures import FilterView
from fdatool.widgets.inputs import LabeledComboBoxText
from fdatool.widgets.specs import AmplitudeSpecs, FrequencySpecs

filter_types = {
    'Butterworth': 'butter',
    'Chebyshev I': 'cheby1',
    'Chebyshev II': 'cheby2',
    'Cauer / Elliptic': 'ellip',
    'Bessel / Thomson': 'bessel',
}

frequency_states = {
    'manual': {
        'Lowpass': ['Fc'],
        'Highpass': ['Fc'],
        'Bandpass': ['Fc1', 'Fc2'],
        'Bandstop': ['Fc1', 'Fc2'],
    },
    'minimum': {
        'Lowpass': ['Fpass', 'Fstop'],
        'Highpass': ['Fstop', 'Fpass'],
        'Bandpass': ['Fstop1', 'Fpass1', 'Fpass2', 'Fstop2'],
        'Bandstop': ['Fpass1', 'Fstop1', 'Fstop2', 'Fpass2'],
    },
}

amplitude_states = {
    'manual': {
        'butter': [],
        'cheby1': ['Rpass'],
        'cheby2': ['Rstop'],
        'ellip': ['Rpass', 'Rstop'],
        'bessel': [],
    },
    'minimum': {
        'butter': ['Gpass', 'Gstop'],
        'cheby1': ['Gpass', 'Gstop'],
        'cheby2': ['Gpass', 'Gstop'],
        'ellip': ['Gpass', 'Gstop'],
        'bessel': ['Gpass', 'Gstop'],
    },
}


class IIR(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self, spacing=4)

        self.response_type = LabeledComboBoxText(label='Response type', options=frequency_states['minimum'].keys())
        self.filter_type = LabeledComboBoxText(label='Filter type', options=filter_types.keys())
        self.filter_order = FilterOrder()
        self.frequency_specs = FrequencySpecs(state=self.response_type.value, states=frequency_states['minimum'])
        self.amplitude_specs = AmplitudeSpecs(state=filter_types[self.filter_type.value], states=amplitude_states['minimum'])

        @self.response_type.changed.register
        def set_frequency_specs_state(response_type):
            self.frequency_specs.state = response_type

        @self.filter_type.changed.register
        def on_change_filter_type(filter_type):
            order = 'minimum' if self.filter_order.minimum.value else 'manual'
            self.amplitude_specs.states = amplitude_states[order]

            filter_type = filter_types[filter_type]
            self.amplitude_specs.state = filter_type

            if len(self.amplitude_specs.states[self.amplitude_specs.state]) == 0:
                self.amplitude_specs.hide()
            else:
                self.amplitude_specs.show()

        @self.filter_order.minimum.changed.register
        def on_change_order_type(minimum_order):
            order = 'minimum' if minimum_order else 'manual'
            filter_type = filter_types[self.filter_type.value]

            self.frequency_specs.states = frequency_states[order]
            self.amplitude_specs.states = amplitude_states[order]
            self.amplitude_specs.state = filter_type

            if len(self.amplitude_specs.states[self.amplitude_specs.state]) == 0:
                self.amplitude_specs.hide()
            else:
                self.amplitude_specs.show()

        self.pack_start(self.response_type, expand=False, fill=True, padding=0)
        self.pack_start(self.filter_type, expand=False, fill=True, padding=0)
        self.pack_start(self.filter_order, expand=False, fill=True, padding=0)
        self.pack_start(self.frequency_specs, expand=False, fill=True, padding=0)
        self.pack_start(self.amplitude_specs, expand=False, fill=True, padding=0)

    @property
    def params(self):
        N = self.filter_order.value

        frequency_specs = self.frequency_specs.values
        unit = frequency_specs.pop('unit')
        scale = frequency_units[unit]
        frequency_specs = {key: scale(value) for key, value in frequency_specs.items()}

        fs = frequency_specs.pop('Fs')

        amplitude_specs = self.amplitude_specs.values
        unit = amplitude_specs.pop('unit')
        scale = amplitude_units[unit]
        amplitude_specs = {key: scale(value) for key, value in amplitude_specs.items()}

        if isinstance(N, int):
            Wn = tuple(frequency_specs.values())

            btype = self.response_type.value.lower()
            ftype = filter_types[self.filter_type.value]

            filter_type = filter_types[self.filter_type.value]
            options = {}

            if filter_type in ('cheby1', 'ellip'):
                options['rp'] = amplitude_specs['Rpass']
            if filter_type in ('cheby2', 'ellip'):
                options['rs'] = amplitude_specs['Rstop']

            return {
                'N': N,
                'Wn': Wn,
                'btype': btype,
                'ftype': ftype,
                'fs': fs,
                **options,
            }
        else:
            response_type = self.response_type.value.lower()

            if response_type in ('lowpass', 'highpass'):
                wp = frequency_specs['Fpass']
                ws = frequency_specs['Fstop']
            elif response_type in ('bandpass', 'bandstop'):
                wp = frequency_specs['Fpass1'], frequency_specs['Fpass2']
                ws = frequency_specs['Fstop1'], frequency_specs['Fstop2']

            return {
                'wp': wp,
                'ws': ws,
                'gpass': amplitude_specs['Gpass'],
                'gstop': amplitude_specs['Gstop'],
                'ftype': filter_types[self.filter_type.value],
                'fs': fs,
            }

    def design(self, params):
        if 'N' in params:
            return signal.iirfilter(**params)
        return signal.iirdesign(**params)

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    specs_label = Gtk.Label()
    specs_label.set_markup('<b>Filter specifications</b>')

    iir = IIR()

    design_button = Gtk.Button(label='Design')

    filter_view = FilterView()

    def on_clicked_design(*args):
        params = iir.params
        print(params)

        dt = 1 / params['fs']

        system = iir.design(params)
        system = signal.dlti(*system, dt=dt)

        filter_view.system = system

    design_button.connect('clicked', on_clicked_design)

    vbox = Gtk.VBox(spacing=4, margin=4)
    vbox.pack_start(specs_label, expand=False, fill=True, padding=10)
    vbox.pack_start(iir, expand=False, fill=True, padding=0)
    vbox.pack_start(design_button, expand=False, fill=True, padding=0)

    hbox = Gtk.HBox(spacing=4, margin=4)
    hbox.pack_start(vbox, expand=False, fill=True, padding=0)
    hbox.pack_start(Gtk.VSeparator(), expand=False, fill=True, padding=4)
    hbox.pack_start(filter_view, expand=True, fill=True, padding=0)

    window.add(hbox)

    window.show_all()

    Gtk.main()
