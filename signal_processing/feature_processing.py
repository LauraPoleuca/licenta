from typing import List
import scipy
import numpy as np
from utils.signal_constants import SAMPLING_HIGHER_BOUND, SAMPLING_LOWER_BOUND, SAMPLING_RATE, BandType
import statsmodels.api as sm


def get_signal_psd(signal, bandType: BandType) -> float:
    f, psd = scipy.signal.welch(signal, SAMPLING_RATE, scaling='spectrum')
    scaled_low = int(bandType.low_frequency * 2)
    scaled_high = int(bandType.high_frequency * 2)
    return np.max(psd[scaled_low: scaled_high])


def get_approximate_entropy(signal) -> float:
    sample = extract_sample(signal)
    r = 0.2 * np.std(sample)
    return approx_entropy(sample, 2, r)


def get_sample_entropy(signal) -> float:
    sample = extract_sample(signal)
    r = 0.2 * np.std(sample)
    return sampen(sample, 2, r)


def get_root_mean_square(signal) -> float:
    return np.sqrt(np.mean([x ** 2 for x in signal]))


def get_autocorrelation(signal) -> float:
    autocorr = sm.tsa.acf(signal)
    return np.average(autocorr)


def approx_entropy(signal, m, r) -> float:

    def _maxdist(x_i, x_j):
        return np.max([abs(ua - va) for ua, va in zip(x_i, x_j)])

    def _phi(m):
        x = [[signal[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [
            len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0)
            for x_i in x
        ]
        return (N - m + 1.0) ** (-1) * sum(np.log(C))

    N = len(signal)

    return abs(_phi(m + 1) - _phi(m))


def sampen(L, m, r) -> float:

    N = len(L)
    B = 0.0
    A = 0.0

    xmi = np.array([L[i: i + m] for i in range(N - m)])
    xmj = np.array([L[i: i + m] for i in range(N - m + 1)])

    B = np.sum([np.sum(np.abs(xmii - xmj).max(axis=1) <= r) - 1 for xmii in xmi])

    m += 1
    xm = np.array([L[i: i + m] for i in range(N - m + 1)])

    A = np.sum([np.sum(np.abs(xmi - xm).max(axis=1) <= r) - 1 for xmi in xm])

    return -np.log(A / B)


def extract_sample(signal) -> List:
    return signal[SAMPLING_LOWER_BOUND:SAMPLING_HIGHER_BOUND]
