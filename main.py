import pickle as pk
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


def read_file(file_path: str, channels: list[str]):
    try:
        channel_data_list = []
        file_data = pk.load(open(file_path, "rb"), encoding="latin1")
        for trial_content in file_data["data"]:
            for channel in channels:
                channel_index = constants.CHANNEL_INDEXES[channel]
                channel_data_list.append(ChannelData(channel, trial_content[channel_index]))
        return channel_data_list
    except KeyError:
        print("Error while processing for one of the given channels")
    except Exception as ex:
        raise ex


def main():
    for channel_data in read_file("s01.dat", ["Fp1"]):
        print(channel_data.channel_name)
        for value in channel_data.channel_values:
            print(value)


if __name__ == '__main__':
    main()
