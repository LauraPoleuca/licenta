import csv
from dataclasses import dataclass
from typing import List

import yaspin

# TODO: change naming or drop the constants directly
import utils.signal_constants as signal_constants
import raw_data_extraction.data_extraction_helper as helper


@dataclass
class PreprocessedData:
    content: any
    labels: any


@dataclass
class ChannelData:
    channel_name: str
    channel_values: list[float]


@dataclass
class TrialData:
    trial_number: int
    data: list[ChannelData]


def read_file(file_name: str, channels: list[str]) -> List:
    """
    for a given user file and a list of channels, returns a list of trials that contains the data for the given channels
    """
    trial_list: list[TrialData] = []
    file_data = helper.read_binary_file(file_name)
    for index, trial_content in enumerate(file_data["data"]):
        trial = TrialData(index, [])
        for channel in channels:
            channel_index = signal_constants.CHANNEL_INDEXES[channel]
            trial.data.append(ChannelData(
                channel, trial_content[channel_index]))
        trial_list.append(trial)
    return trial_list

def write_user_files(user: str, trial_data_list: list[TrialData]) -> None:
    """
    creates a folder with the given user name and creates .csv files with the data from the given TrialData list
    """
    helper.create_user_folder(user)
    for index, trial in enumerate(trial_data_list):
        file_name = helper.get_user_trial_filename(user, index)
        write_data_to_file(file_name, trial)


def write_data_to_file(file_path: str, trial_data: TrialData) -> None:
    """
    in the given path it creates a .csv file containing the information from the given TrialData
    """
    rows = map(
        lambda channel_data: [channel_data.channel_name] +
        list(map(lambda x: str(x), channel_data.channel_values)),
        trial_data.data)
    file = open(file_path, 'w', newline='')
    writer = csv.writer(file)
    for column in zip(*rows):
        writer.writerow(column)
    file.close()


def process_raw_data() -> None:
    """
    resets the output folder and
    """
    helper.reset_output_folder()
    for file in helper.get_user_input_files():
        trials = read_file(file, signal_constants.CHANNEL_INDEXES.keys())
        with yaspin.yaspin(text=f"Processing file {file}") as sp:
            write_user_files(helper.get_username_from_file(file), trials)
            sp.write(f"File {file} finished processing successfully ✔")


if __name__ == '__main__':
    process_raw_data()
    print("Process finished successfully")
