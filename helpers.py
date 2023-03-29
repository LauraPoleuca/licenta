import os
import constants

def get_file_names():
    return os.listdir(os.path.join(".", constants.USER_FILE_DIRECTORY_NAME))

