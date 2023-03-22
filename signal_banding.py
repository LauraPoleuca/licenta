import os

import numpy as np
import scipy.signal as signal
import constants
import matplotlib.pyplot as plt

from enum import Enum

class BandEnum(Enum):
    ALPHA = 1,
    BETA = 2,
    GAMMA = 3


class BandType:
    def __init__(self, band_enum: BandEnum, low_frequency: float, high_frequency: float) -> None:
        self.enum_type = band_enum
        self.low_frequency = low_frequency
        self.high_frequency = high_frequency


def get_filter_polynomials(lowcut_frequency: float, highcut_frequency: float, sampling_frequency: int, filter_order: int) -> tuple():
    nyquist_frequency = 0.5 * sampling_frequency
    lowcut_nyquist =  lowcut_frequency / nyquist_frequency
    highcut_nyquist = highcut_frequency / nyquist_frequency
    numerator, denominator = signal.butter(filter_order, [lowcut_nyquist, highcut_nyquist], btype='bandpass')
    return numerator, denominator


def filter(eeg_signal: any, band: BandType) -> any:
    sampling_frequency = 128
    filter_order = 5
    numerator, denominator = get_filter_polynomials(band.low_frequency, band.high_frequency, sampling_frequency, filter_order)
    return signal.lfilter(numerator, denominator, eeg_signal)


def get_signal(file_path = "trial1.csv", channel_name = "Fp1"):
    file_path = os.path.join(".", constants.USER_OUTPUT_DIRECTORY_NAME, "s02", "trial_11.csv")
    channel_name = "F8"
    channel_index = constants.CHANNEL_INDEXES[channel_name] - 1
    file = open(file_path, "r")
    lines = file.readlines()
    lines.pop(0) # remove first line which contains the channel name
    channel_data = list(map(lambda line: float(line.split(",")[channel_index]), lines))
    return np.array(channel_data[constants.SAMPLING_LOWER_BOUND:constants.SAMPLING_HIGHER_BOUND])


def plot_signal(filtered_signal):
    plt.rcParams["figure.figsize"] = [15, 7]
    plt.rcParams["figure.autolayout"] = True
    t = np.arange(0, constants.SAMPLING_HIGHER_BOUND - constants.SAMPLING_LOWER_BOUND)
    _, axs = plt.subplots()
    axs.set_title("Signal")
    axs.plot(t, filtered_signal, color='g')
    axs.set_xlabel("Time")
    axs.set_ylabel("Amplitude")
    plt.show()


def main():
    alpha_band_type = BandType(BandEnum.ALPHA, 7.5, 12.5)
    beta_band_type = BandType(BandEnum.ALPHA, 13.0, 30.0)
    gamma_band_type = BandType(BandEnum.ALPHA, 30.0, 63.5)

    eeg_signal = get_signal()
    filtered_signal = filter(eeg_signal, alpha_band_type)
    plot_signal(filtered_signal)
    filtered_signal = filter(eeg_signal, beta_band_type)
    plot_signal(filtered_signal)
    filtered_signal = filter(eeg_signal, gamma_band_type)
    plot_signal(filtered_signal)

main()