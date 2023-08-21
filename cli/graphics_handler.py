import json
from typing import List

import inquirer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from cli.classifiers_handler import get_input_models

from cli.cli_constants import FEATURE_IDENTIFIERS, GraphingOptions
from graphing.histogram_plotter import plot_histograms
from graphing.signal_plotter import plot_comparison, plot_signal
import raw_data_extraction.data_extraction_helper as helper
from utils.data_extraction_constants import DATA, TRAINED_MODEL_FILE
from utils.signal_constants import ALPHA_BAND_TYPE, BETA_BAND_TYPE, CHANNEL_INDEXES, GAMMA_BAND_TYPE
import signal_processing.band_processing as band_processor


def get_options() -> List[str]:
    return [
        GraphingOptions.Signal_Banding,
        GraphingOptions.Naive_Bayes_Classifier_Histogram
    ]


def handle_graphics():
    option = inquirer.list_input("Entity to preview", choices=get_options())
    match option:
        case GraphingOptions.Signal_Banding:
            handle_signal_banding_graphing()
        case GraphingOptions.Naive_Bayes_Classifier_Histogram:
            handle_naive_bayes_histogram_graphing()


def handle_signal_banding_graphing():
    file_name = "s01.dat"
    file_content = helper.read_binary_file(file_name)[DATA]
    username = helper.get_username_from_file(file_name).lower()
    trial_index = 0
    channel_signals = file_content[trial_index]
    channel = "Fp1"
    channel_index = CHANNEL_INDEXES[channel] - 1
    raw_channel_signal = channel_signals[channel_index]
    alpha_banded_signal = band_processor.filter(raw_channel_signal, ALPHA_BAND_TYPE)
    beta_banded_signal = band_processor.filter(raw_channel_signal, BETA_BAND_TYPE)
    gamma_banded_signal = band_processor.filter(raw_channel_signal, GAMMA_BAND_TYPE)
    plot_signal(alpha_banded_signal, ALPHA_BAND_TYPE, username, trial_index, channel)
    plot_signal(beta_banded_signal, BETA_BAND_TYPE, username, trial_index, channel)
    plot_signal(gamma_banded_signal, GAMMA_BAND_TYPE, username, trial_index, channel)
    plot_comparison(['alpha', 'beta', 'gamma'], [alpha_banded_signal, beta_banded_signal, gamma_banded_signal])


def handle_naive_bayes_histogram_graphing():
    channel_option, feature_option, band_option = get_histogram_options()
    histogram_data = get_histogram_data(channel_option, feature_option, band_option)
    input_models = get_input_models()
    nbc = NaiveBayesClassifier.default()
    nbc.train_classifier(input_models)
    feature_interval = nbc.intervals[f"{channel_option}-{band_option}-{FEATURE_IDENTIFIERS[feature_option]}"]
    plot_histograms(channel_option, feature_option, band_option, histogram_data, feature_interval)


def get_histogram_data(channel_option, feature_option, band_option):
    translated_feature_option = FEATURE_IDENTIFIERS[feature_option]
    data_key = f"{channel_option}-{band_option}-{translated_feature_option}"
    with open(TRAINED_MODEL_FILE, 'r') as file:
        serialized_model = json.load(file)
        return serialized_model[data_key]
    

def get_histogram_options():
    channel_option = inquirer.list_input("Channel", choices=CHANNEL_INDEXES.keys())
    feature_option = inquirer.list_input("Feature", choices=FEATURE_IDENTIFIERS.keys())
    # feature_option = FEATURE_IDENTIFIERS[feature_option]
    band_option = inquirer.list_input("Band", choices=["alpha", "beta"])
    return channel_option, feature_option, band_option
