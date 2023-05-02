import os
from raw_data_extraction.raw_data_processor import process_raw_data
from signal_processing.band_processing import *
from graphing.grapher import plot_signal
from data_access.data_access_service import DataAccessService
from signal_processing.feature_processing import get_signal_psd
import utils.database_constants as dbc


def test_signal_filter_and_graph():
    eeg_signal = get_signal("s01", "trial_1.csv", "Fp1")
    filtered_signal = filter(eeg_signal, ALPHA_BAND_TYPE)
    plot_signal(filtered_signal)


def test_data_insertion():
    os.remove(dbc.DATABASE_PATH)
    data_access_service = DataAccessService()
    data_access_service.initialize_database()
    eeg_signal = get_signal("s01", "trial_1.csv", "Fp1")
    filtered_signal = filter(eeg_signal, ALPHA_BAND_TYPE)
    psd = get_signal_psd(filtered_signal, ALPHA_BAND_TYPE)
    print(psd)


def main():
    # process_raw_data()
    # test_signal_filter_and_graph()
    test_data_insertion()
    pass


if __name__ == "__main__":
    main()
    print("ok")
