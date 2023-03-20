import pickle as pk
import os
import csv
import shutil
from dataclasses import dataclass

import constants

"""
use pickle to read binary file
    data: 40 trials x 40 channels x (63 * 128)
    labels: 40 trials x 4 label values
create dataclasses for the entities
a method that given a file and a selection of channels can extract the data and put it into an object
a method that given the object can write it into a file (csv most likely)
a method that allows for the processing of multiple files in a given directory
"""


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


def read_file(file_name: str, channels: list[str]):
    try:
        trial_list: list[TrialData] = []
        file_path = os.path.join(".", constants.USER_FILE_DIRECTORY_NAME, file_name)
        file_data = pk.load(open(file_path, "rb"), encoding="latin1")
        for index, trial_content in enumerate(file_data["data"]):
            trial = TrialData(index, [])
            for channel in channels:
                channel_index = constants.CHANNEL_INDEXES[channel]
                trial.data.append(ChannelData(channel, trial_content[channel_index]))
            trial_list.append(trial)
        return trial_list
    except KeyError:
        print("Error while processing for one of the given channels")
    except Exception as ex:
        raise ex


def get_file_names():
    return os.listdir(os.path.join(".", constants.USER_FILE_DIRECTORY_NAME))


def write_user_files(user: str, trial_data_list: list[TrialData]):
    user_dir = os.path.join(".", constants.USER_OUTPUT_DIRECTORY_NAME, user)
    os.mkdir(user_dir)
    for index, trial in enumerate(trial_data_list):
        file_name = os.path.join(user_dir, f"trial_{str(index + 1)}.csv")
        write_data_to_file(file_name, trial)


def write_data_to_file(file_path: str, trial_data: TrialData):
    rows = []
    for channel_data in trial_data.data:
        row = [channel_data.channel_name] + list(map(lambda x: str(x), channel_data.channel_values))
        rows.append(row)

    f = open(file_path, 'w', newline='')
    writer = csv.writer(f)

    # writing by columns is done by transposing the rows and treating the results as columns
    for column in zip(*rows):
        writer.writerow(column)
    f.close()


def clear_output_file():
    output_file_path = os.path.join(".", constants.USER_OUTPUT_DIRECTORY_NAME)
    shutil.rmtree(output_file_path)
    os.mkdir(output_file_path)


def main():
    clear_output_file()
    for file in get_file_names():
        trials = read_file(file, constants.CHANNEL_INDEXES.keys())
        write_user_files(file.replace(".dat", ""), trials)
    print("Process finished successfully")


if __name__ == '__main__':
    main()
