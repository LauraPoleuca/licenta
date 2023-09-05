import json
from typing import List
from data_access.models.input_model import InputModel

import raw_data_extraction.data_extraction_helper as helper
import signal_processing.band_processing as band_processor
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from cli.cli_constants import FEATURE_IDENTIFIERS
from graphing.histogram_plotter import plot_histograms
from graphing.signal_plotter import plot_comparison, plot_signal
from utils.data_extraction_constants import DATA, TRAINED_MODEL_FILE
from utils.signal_constants import (ALPHA_BAND_TYPE, BETA_BAND_TYPE,
                                    CHANNEL_INDEXES, GAMMA_BAND_TYPE)


class GraphicsService:

    def display_signal_banding_graph(self, file_name: str, trial_index: int, channel: str):
        file_content = helper.read_binary_file(file_name)[DATA]
        username = helper.get_username_from_file(file_name).lower()
        channel_signals = file_content[trial_index]
        channel_index = CHANNEL_INDEXES[channel] - 1
        raw_channel_signal = channel_signals[channel_index]

        alpha_banded_signal = band_processor.filter(raw_channel_signal, ALPHA_BAND_TYPE)
        beta_banded_signal = band_processor.filter(raw_channel_signal, BETA_BAND_TYPE)
        # gamma_banded_signal = band_processor.filter(raw_channel_signal, GAMMA_BAND_TYPE)

        plot_signal(alpha_banded_signal, ALPHA_BAND_TYPE, username, trial_index, channel)
        plot_signal(beta_banded_signal, BETA_BAND_TYPE, username, trial_index, channel)
        # plot_signal(gamma_banded_signal, GAMMA_BAND_TYPE, username, trial_index, channel)
        # plot_comparison(['alpha', 'beta', 'gamma'], [alpha_banded_signal, beta_banded_signal, gamma_banded_signal])
        plot_comparison(['alpha', 'beta'], [alpha_banded_signal, beta_banded_signal])

    def display_nbc_histogram(self, channel_option: str, feature_option: str, band_option: str,
                              input_models: List[InputModel]):
        histogram_data = self.__get_histogram_data(channel_option, feature_option, band_option)
        nbc = NaiveBayesClassifier.default()
        nbc.train_classifier(input_models)
        feature_interval = nbc.intervals[f"{channel_option}-{band_option}-{FEATURE_IDENTIFIERS[feature_option]}"]
        plot_histograms(channel_option, feature_option, band_option, histogram_data, feature_interval)

    def __get_histogram_data(self, channel_option, feature_option, band_option):
        translated_feature_option = FEATURE_IDENTIFIERS[feature_option]
        data_key = f"{channel_option}-{band_option}-{translated_feature_option}"
        with open(TRAINED_MODEL_FILE, 'r') as file:
            serialized_model = json.load(file)
            return serialized_model[data_key]
