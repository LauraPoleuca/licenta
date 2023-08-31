from typing import List, Tuple

import inquirer

from business_logic.graphics_service import GraphicsService
from cli.classifiers_handler import get_input_models
from cli.cli_constants import FEATURE_IDENTIFIERS, GraphingOptions
from utils.signal_constants import CHANNEL_INDEXES


def get_options() -> List[str]:
    return [
        GraphingOptions.Signal_Banding,
        GraphingOptions.Naive_Bayes_Classifier_Histogram
    ]


def handle_graphics() -> None:
    option = inquirer.list_input("Alegeti entitatea de previzualizat", choices=get_options())
    match option:
        case GraphingOptions.Signal_Banding:
            handle_signal_banding_graphing()
        case GraphingOptions.Naive_Bayes_Classifier_Histogram:
            handle_naive_bayes_histogram_graphing()


def handle_signal_banding_graphing() -> None:
    graphics_service = GraphicsService()
    file_name = "s01.dat"
    trial_index = 0
    channel = "Fp1"
    graphics_service.display_signal_banding_graph(file_name, trial_index, channel)


def handle_naive_bayes_histogram_graphing() -> None:
    channel_option, feature_option, band_option = get_histogram_options()
    input_models = get_input_models()
    graphics_service = GraphicsService()
    graphics_service.display_nbc_histogram(channel_option, feature_option, band_option, input_models)


def get_histogram_options() -> Tuple[str, str, str]:
    channel_option = inquirer.list_input("Canal", choices=CHANNEL_INDEXES.keys())
    feature_option = inquirer.list_input("Trasatura", choices=FEATURE_IDENTIFIERS.keys())
    # feature_option = FEATURE_IDENTIFIERS[feature_option]
    band_option = inquirer.list_input("Banda", choices=["alpha", "beta"])
    return channel_option, feature_option, band_option
