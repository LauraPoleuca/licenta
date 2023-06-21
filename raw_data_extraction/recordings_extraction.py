import multiprocessing as mp
import time
from typing import List

from data_access.models.recording import Recording
from data_access.models.trial import Trial
import raw_data_extraction.data_extraction_helper as helper
import signal_processing.band_processing as band_processor
import signal_processing.feature_processing as feature_processor
from utils.data_extraction_constants import DATA
from utils.signal_constants import ALPHA_BAND_TYPE, BETA_BAND_TYPE, CHANNEL_INDEXES, GAMMA_BAND_TYPE, BandType


def get_recordings_multiprocessing(channel_list, trial_list):
    optimized_arguments = get_multiprocessing_arguments(channel_list, trial_list)
    with mp.Pool() as pool:
        start = time.time()
        results = pool.starmap(optimized_get_user_trial_recordings, optimized_arguments)
        end = time.time()
        print(end - start)
        return sum(results, [])


def optimized_get_user_trial_recordings(file_name, trial_index, channel_list):
    file_content = helper.read_binary_file(file_name)[DATA]
    username = helper.get_username_from_file(file_name).lower()
    return get_user_trial_recordings(username, file_content, trial_index, channel_list)


def get_user_recordings(file_name, channel_list):
    file_content = helper.read_binary_file(file_name)[DATA]
    trial_indexes = list(range(40))
    username = helper.get_username_from_file(file_name).lower()
    print(f"Processing file {file_name}")
    return sum(map(lambda trial_index: get_user_trial_recordings(username, file_content, trial_index, channel_list), trial_indexes), [])


def get_user_trial_recordings(username, file_content, trial_index, channel_list):
    print(f"starting for {username} {trial_index}")
    channel_signals = file_content[trial_index]
    recordings = []
    for channel in channel_list:
        channel_index = CHANNEL_INDEXES[channel]
        raw_channel_signal = channel_signals[channel_index]
        alpha_features = get_feature_list(raw_channel_signal, ALPHA_BAND_TYPE)
        beta_features = get_feature_list(raw_channel_signal, BETA_BAND_TYPE)
        gamma_features = get_feature_list(raw_channel_signal, GAMMA_BAND_TYPE)
        recording = Recording(channel, username, trial_index + 1, alpha_features, beta_features, gamma_features)
        recordings.append(recording)
    return recordings


def get_feature_list(raw_signal, band_type: BandType):
    banded_signal = band_processor.filter(raw_signal, band_type)
    psd = feature_processor.get_signal_psd(banded_signal, band_type)
    ae = feature_processor.get_approximate_entropy(banded_signal)
    se = feature_processor.get_sample_entropy(banded_signal)
    rms = feature_processor.get_root_mean_square(banded_signal)
    corr = feature_processor.get_autocorrelation(banded_signal)
    return [se, ae, psd, rms, corr]


def get_multiprocessing_arguments(channel_list, trials: List[Trial] = []):
    # files = helper.get_user_input_files()
    users = []
    trial_indexes = []
    channel_lists = []
    # for file in files:
        # indexes = list(range(40))
        # for trial_index in indexes:
            # users.append(file)
            # trial_indexes.append(trial_index)
            # channel_lists.append(channel_list)
    for trial in trials:
        users.append(trial.user_id + ".dat")
        trial_indexes.append(trial.trial_id - 1)
        channel_lists.append(channel_list)
    return zip(users, trial_indexes, channel_lists)
