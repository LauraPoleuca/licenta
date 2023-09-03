import scipy.signal as signal
import numpy as np

from utils.signal_constants import *


def get_filter_polynomials(
        lowcut_frequency: float, highcut_frequency: float, sampling_frequency: int, filter_order: int) -> tuple:
    nyquist_frequency = 0.5 * sampling_frequency
    lowcut_nyquist = lowcut_frequency / nyquist_frequency
    highcut_nyquist = highcut_frequency / nyquist_frequency
    numerator, denominator = signal.cheby2(
        filter_order, 3, [lowcut_nyquist, highcut_nyquist], btype='bandpass')
    return numerator, denominator


def filter(eeg_signal: any, band: BandType) -> np.ndarray:
    numerator, denominator = get_filter_polynomials(
        band.low_frequency, band.high_frequency, SAMPLING_RATE, FILTER_ORDER)
    return signal.lfilter(numerator, denominator, eeg_signal)
