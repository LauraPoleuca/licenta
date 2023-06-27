import csv
from dataclasses import dataclass

# TODO: change naming or drop the constants directly
import utils.data_extraction_constants as extraction_constants
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
    helper.create_user_folder(user)
    for index, trial in enumerate(trial_data_list):
        file_name = helper.get_user_trial_filename(user, index)
        write_data_to_file(file_name, trial)


def write_data_to_file(file_path: str, trial_data: TrialData) -> None:
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
    helper.reset_output_file()
    for file in helper.get_user_input_files():
        trials = read_file(file, signal_constants.CHANNEL_INDEXES.keys())
        write_user_files(helper.get_username_from_file(file), trials)


if __name__ == '__main__':
    process_raw_data()
    print("Process finished successfully")
