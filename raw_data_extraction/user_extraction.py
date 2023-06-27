from typing import List
from pyexcel_ods3 import get_data
from data_access.models.user import User

def get_users() -> List:
    data = get_data("participant_questionnaire.ods")
    user_records = list(data["Sheet1"])
    user_records.pop(0)
    user_records = filter(lambda user_rec: user_rec != [], user_records)
    return list(map(lambda user_rec: User(user_rec[0].lower(), user_rec[2]), user_records))