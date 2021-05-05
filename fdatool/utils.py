import math


class Event(object):
    def __init__(self):
        self.callbacks = []

    def register(self, callback):
        self.callbacks.append(callback)
        return callback

    def notify(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)


def scale(factor):
    def multiply(value):
        try:
            return factor * float(value)
        except:
            return None
    return multiply


frequency_units = {
    'Hz': scale(1),
    'kHz': scale(1e3),
    'MHz': scale(1e6),
    'GHz': scale(1e9),
}

amplitude_units = {
    'dB': lambda x: x,
    'V': lambda x: 20 * math.log(x, 10),
    'W': lambda x: 10 * math.log(x, 10),
}
