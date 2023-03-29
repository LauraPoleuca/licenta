import pickle as pk

from models import *
from helpers import *
from models.recording import Recording
from models.trial import Trial

# def read_file(file_name: str, channels: list[str]):
#     trials = []
#     file_path = os.path.join(".", constants.USER_FILE_DIRECTORY_NAME, file_name)
#     file_data = pk.load(open(file_path, "rb"), encoding="latin1")
#     for index, ratings in file_data["labels"]:
#         trials.append(Trial(file_name, index))
    
def get_user_trials(file_name: str):
    trials = []
    file_path = os.path.join(".", constants.USER_FILE_DIRECTORY_NAME, file_name)
    file_data = pk.load(open(file_path, "rb"), encoding="latin1")
    for index, ratings in enumerate(file_data["labels"]):
        trials.append(Trial(file_name.replace(".dat", ""), index, ratings[0], ratings[1]))
    return trials

def get_user_recordings(file_name: str, channels = constants.CHANNEL_INDEXES.keys()):
    recordings = []
    file_path = os.path.join(".", constants.USER_FILE_DIRECTORY_NAME, file_name)
    file_data = pk.load(open(file_path, "rb"), encoding="latin1")
    for index, trial_content in enumerate(file_data["data"]):
            trial_id = index + 1
            for channel in channels:
                channel_index = constants.CHANNEL_INDEXES[channel]
                #TODO: determine the value of the signal features
                recordings.append(Recording(channel, file_name.replace(".dat", ""), trial_id, [0,0,0,0], [0,0,0,0], [0,0,0,0]))
    return recordings