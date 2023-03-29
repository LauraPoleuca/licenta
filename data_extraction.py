import os
from data_access.data_access_service import DataAccessService
import database_constants as dbc
from helpers import get_file_names
from model_reader import get_user_recordings, get_user_trials
from models.recording import Recording
from models.trial import Trial
from models.user import User
from user_reader import get_users

class DataExtractionService:
    data_service : DataAccessService

    def __init__(self) -> None:
        self.data_service = DataAccessService()

    def initialize_database(self):
        self.data_service.initialize_database()

    def initialize_mock_data(self):
        # users = [
        #     User("s01", "male"),
        #     User("s02", "female")
        # ]
        # trials = [
        #     Trial("s01", 1),
        #     Trial("s01", 2),
        #     Trial("s01", 3),
        #     Trial("s02", 1)
        # ]
        # recordings = [
        #     Recording(1, "s01", 1, 4.5, 8.9),
        #     Recording(2, "s01", 1, 9.9, 3.4)
        # ]
        # self.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_USERS, users)
        # self.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_TRIALS, trials)
        # self.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_RECORDINGS, recordings)
        pass

    def add_users(self):
        users = get_users()
        self.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_USERS, users)

    def add_trials(self):
        trials = []
        for filename in get_file_names():
            trials += get_user_trials(filename)
        self.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_TRIALS, trials)

    def add_recordings(self):
        recordings = []
        for filename in get_file_names():
            recordings += get_user_recordings(filename)
        self.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_RECORDINGS, recordings)

    def clear_database(self):
        self.data_service.clear_database()


os.remove(dbc.DATABASE_PATH)
data_extraction_service = DataExtractionService()
data_extraction_service.initialize_database()
#data_extraction_service.initialize_mock_data()
#data_extraction_service.clear_database()
data_extraction_service.add_users()
data_extraction_service.add_trials()
data_extraction_service.add_recordings()


#data_extraction_service.data_service.insert_range_data(dbc.INSERT_RANGE_TABLE_TRIALS, [Trial('a', 'a', 0, 0)])
