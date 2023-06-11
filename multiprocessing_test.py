import multiprocessing as mp
import time

from raw_data_extraction.recordings_extraction import get_user_recordings, get_user_trial_recordings
import raw_data_extraction.data_extraction_helper as helper
from utils.data_extraction_constants import DATA


# if __name__ == '__main__':
#     with mp.Pool() as pool:
#         print("starting...")
#         start = time.time()
#         # fileargs = [("s01.dat", ["Fp1"]), ("s02.dat", ["Fp1"]), ("s03.dat", ["Fp1"])]
#         filenames = ["s01.dat", "s02.dat", "s03.dat"]
#         channel_lists = [["Fp1"], ["Fp1"], ["Fp1"]]
#         arguments = zip(filenames, channel_lists)
#         user_recordings = pool.starmap(get_user_recordings, arguments)
#         end = time.time()
#         print(end - start)


def optimized_get_user_trial_recordings(file_name, trial_index, channel_list):
    file_content = helper.read_binary_file(file_name)[DATA]
    username = helper.get_username_from_file(file_name).lower()
    return get_user_trial_recordings(username, file_content, trial_index, channel_list)


if __name__ == '__main__':
    users = []
    usernames = []
    file_contents = []
    trial_indexes = []
    channel_lists = []
    for user in ["s01.dat", "s02.dat", "s03.dat"]:
        file_content = helper.read_binary_file(user)[DATA]
        indexes = list(range(40))
        username = helper.get_username_from_file(user).lower()
        for trial_index in indexes:
            users.append(user)
            usernames.append(username)
            file_contents.append(file_content)
            trial_indexes.append(trial_index)
            channel_lists.append(["Fp1"])
    # arguments = zip(usernames, file_contents, trial_indexes, channel_lists)
    optimized_arguments = zip(users, trial_indexes, channel_lists)
    with mp.Pool() as pool:
        start = time.time()
        # pool.starmap(get_user_trial_recordings, arguments)
        pool.starmap(optimized_get_user_trial_recordings, optimized_arguments)
        end = time.time()
        print(end - start)
