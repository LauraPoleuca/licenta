import os
import time
from data_access.models.trial import Trial
from raw_data_extraction.recordings_extraction import get_recordings_multiprocessing
from raw_data_extraction.trial_extraction import get_trials
import utils.database_constants as dbc
from raw_data_extraction.user_extraction import get_users
from data_access.data_access_service import DataAccessService
from utils.signal_constants import CHANNEL_INDEXES


class DatabaseGenerationService:

    def __init__(self):
        pass

    def insert_users(data_access_service: DataAccessService) -> None:
        """
        Description - what the method does
            - data_access_service: service responsible for inserting the data in the db
            - outputs: None
        """
        users = get_users()
        data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_USERS, users)

    def insert_trials(data_access_service: DataAccessService) -> None:
        trials = get_trials(quadrant_filtering=True)
        data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_TRIALS, trials)

    def insert_recordings(data_access_service: DataAccessService) -> None:
        trials = data_access_service.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
        recordings = get_recordings_multiprocessing(list(CHANNEL_INDEXES.keys()), trials)
        data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_RECORDINGS, recordings)

    def populate_database(self):
        start = time.time()
        os.remove(dbc.DATABASE_PATH)
        data_access_service = DataAccessService()
        data_access_service.initialize_database()
        self.insert_users(data_access_service)
        self.insert_trials(data_access_service)
        self.insert_recordings(data_access_service)
        end = time.time()
        print(f"Executia a durat {end - start} secunde")
