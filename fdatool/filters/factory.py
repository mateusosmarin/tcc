from fdatool.filters.firls import FIRLeastSquares
from fdatool.filters.iir import IIR
from fdatool.filters.remez import Remez

filters = {
    'FIR - Least squares': FIRLeastSquares,
    'FIR - Remez': Remez,
    'IIR': IIR,
}


def build(name):
    return filters[name]()
