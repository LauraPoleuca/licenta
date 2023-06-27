from typing import List
import os
import shutil
import pickle as pk

from utils.data_extraction_constants import *


def get_relative_file_path(*arguments) -> str:
    """
    creates the relative path for a file
    """
    # print(os.getcwd())
    x = os.path.join(".", *arguments)
    # print(x)
    return x


def get_user_input_files() -> List:
    """
    returns a list of files from a directory
    """
    return os.listdir(get_relative_file_path(USER_FILE_DIRECTORY_NAME))

# this is gonna take a while


def reset_output_file() -> None:
    """
    recursively removes the content from output file and creates a new empty one
    """
    output_file_path = get_relative_file_path(USER_OUTPUT_DIRECTORY_NAME)
    shutil.rmtree(output_file_path)
    os.mkdir(output_file_path)


def create_user_folder(username: str) -> None:
    user_dir = get_relative_file_path(USER_OUTPUT_DIRECTORY_NAME, username)
    os.mkdir(user_dir)


def get_user_trial_filename(username: str, trial: int) -> str:
    local_filename = f"trial_{str(trial + 1)}.csv"
    return get_relative_file_path(USER_OUTPUT_DIRECTORY_NAME, username, local_filename)


def get_username_from_file(filename: str) -> str:
    return filename.replace(".dat", "")


def read_binary_file(file_name: str) -> dict:
    file_path = get_relative_file_path(USER_FILE_DIRECTORY_NAME, file_name)
    return pk.load(open(file_path, BINARY_READ), encoding=LATIN_ENCODING)
