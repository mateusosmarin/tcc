import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import numpy as np
from matplotlib.backends.backend_gtk3 import \
    NavigationToolbar2GTK3 as NavigationToolbar
from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class FilterView(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self, spacing=4, margin=4)

        self.figure = Figure(tight_layout=True)

        self.amplitude_ax = self.figure.add_subplot(2, 2, 1)
        self.phase_ax = self.figure.add_subplot(2, 2, 2)
        self.zpk_ax = self.figure.add_subplot(2, 2, 3)
        self.impulse_ax = self.figure.add_subplot(2, 2, 4)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request(800, 600)

        self.navigation_toolbar = NavigationToolbar(self.canvas, self)

        self.pack_start(self.navigation_toolbar, expand=False, fill=True, padding=0)
        self.pack_start(self.canvas, expand=True, fill=True, padding=0)

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, system):
        self.__system = system
        self.update()

    def update(self):
        w, mag, phase = self.system.bode()

        self.amplitude_ax.clear()
        self.amplitude_ax.plot(w / (2 * np.pi), mag)
        self.amplitude_ax.set_xlabel('f [Hz]')
        self.amplitude_ax.set_ylabel(r'$|H(e^{j 2 \pi f})|^2$ [dB]')
        self.amplitude_ax.grid(True)

        self.phase_ax.clear()
        self.phase_ax.plot(w / (2 * np.pi), phase)
        self.phase_ax.set_xlabel('f [Hz]')
        self.phase_ax.set_ylabel(r'$\phi(e^{j 2 \pi f})$ [deg]')
        self.phase_ax.grid(True)

        zpk = self.system.to_zpk()
        self.zpk_ax.clear()
        self.zpk_ax.scatter(np.real(zpk.zeros), np.imag(
            zpk.zeros), marker='o', label='Zeros')
        self.zpk_ax.scatter(np.real(zpk.poles), np.imag(
            zpk.poles), marker='x', label='Poles')
        self.zpk_ax.set_xlabel(r'$Re\{z\}$')
        self.zpk_ax.set_ylabel(r'$Im\{z\}$')
        self.zpk_ax.legend()
        self.zpk_ax.grid(True)
        self.zpk_ax.set_aspect(1)

        t, h = self.system.impulse()
        self.impulse_ax.clear()
        self.impulse_ax.plot(t, np.squeeze(h))
        self.impulse_ax.set_xlabel('t [s]')
        self.impulse_ax.set_ylabel('h(t) [V]')
        self.impulse_ax.grid(True)

        self.figure.canvas.draw()


if __name__ == '__main__':
    from scipy import signal

    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)

    btype = 'lowpass'
    system = signal.butter(2, 0.5, btype=btype)
    system = signal.dlti(*system)

    filter_view = FilterView()

    button = Gtk.Button(label='lowpass')

    def on_clicked(widget):
        btype = widget.get_label()
        widget.set_label('highpass' if btype == 'lowpass' else 'lowpass')
        system = signal.butter(2, 0.5, btype=btype)
        system = signal.dlti(*system)
        filter_view.system = system

    button.connect('clicked', on_clicked)

    box = Gtk.VBox(spacing=4)

    box.pack_start(filter_view, expand=True, fill=True, padding=0)
    box.pack_start(button, expand=False, fill=True, padding=0)
    window.add(box)

    window.show_all()
    Gtk.main()
