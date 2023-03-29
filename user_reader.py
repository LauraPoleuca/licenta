from pyexcel_ods3 import get_data
from models.user import User

def get_users():
    data = get_data("participant_questionnaire.ods")
    user_records = list(data["Sheet1"])
    user_records.pop(0)
    user_records = filter(lambda user_rec: user_rec != [], user_records)
    return map(lambda user_rec: User(user_rec[0], user_rec[2]), user_records)

#get_users()