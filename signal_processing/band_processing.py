import scipy.signal as signal
import numpy as np

import raw_data_extraction.data_extraction_helper as helper
import utils.data_extraction_constants as extraction_constants
import utils.signal_constants as signal_constants
from utils.signal_constants import *


def get_filter_polynomials(lowcut_frequency: float, highcut_frequency: float, sampling_frequency: int, filter_order: int) -> tuple():
    nyquist_frequency = 0.5 * sampling_frequency
    lowcut_nyquist = lowcut_frequency / nyquist_frequency
    highcut_nyquist = highcut_frequency / nyquist_frequency
    numerator, denominator = signal.butter(
        filter_order, [lowcut_nyquist, highcut_nyquist], btype='bandpass')
    return numerator, denominator


def filter(eeg_signal: any, band: BandType) -> any:
    numerator, denominator = get_filter_polynomials(
        band.low_frequency, band.high_frequency, SAMPLING_RATE, FILTER_ORDER)
    return signal.lfilter(numerator, denominator, eeg_signal)


def get_signal(username: str, file_name: str, channel_name: str):
    file_path = helper.get_relative_file_path(
        extraction_constants.USER_OUTPUT_DIRECTORY_NAME, username, file_name)
    channel_index = signal_constants.CHANNEL_INDEXES[channel_name] - 1
    file = open(file_path, "r")
    lines = file.readlines()
    lines.pop(0)  # remove first line which contains the channel name
    # note: this works only if all the channels are inside the csv file. otherwise please consider a different way of getting the channel index
    channel_data = list(map(lambda line: float(
        line.split(",")[channel_index]), lines))
    return np.array(channel_data[signal_constants.SAMPLING_LOWER_BOUND: signal_constants.SAMPLING_HIGHER_BOUND])
