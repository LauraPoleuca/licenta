from typing import List
from pyexcel_ods3 import get_data
from data_access.models.user import User
from utils.data_extraction_constants import QUESTIONAIRE_NAME, QUESTIONAIRE_SHEET


def get_users() -> List[User]:
    """
    Extracts the information about an user
    """
    data = get_data(QUESTIONAIRE_NAME)
    user_records = list(data[QUESTIONAIRE_SHEET])
    user_records.pop(0)
    user_records = filter(lambda user_rec: user_rec != [], user_records)
    return list(map(lambda user_rec: User(user_rec[0].lower(), user_rec[2]), user_records))
