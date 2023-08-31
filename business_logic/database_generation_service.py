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

    def insert_users(self) -> None:
        """
        Description - what the method does
            - data_access_service: service responsible for inserting the data in the db
            - outputs: None
        """
        users = get_users()
        self.data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_USERS, users)

    def insert_trials(self) -> None:
        trials = get_trials(quadrant_filtering=True)
        self.data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_TRIALS, trials)

    def insert_recordings(self) -> None:
        trials = self.data_access_service.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
        # trials = [Trial('s01', 1, 0, 0, 1), Trial('s01', 2, 0, 0, 1)]
        recordings = get_recordings_multiprocessing(list(CHANNEL_INDEXES.keys()), trials)
        # recordings = get_recordings_multiprocessing(['Fp1'], trials)
        self.data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_RECORDINGS, recordings)

    def populate_database(self):
        start = time.time()
        os.remove(dbc.DATABASE_PATH)
        self.data_access_service = DataAccessService()
        self.data_access_service.initialize_database()
        self.insert_users()
        self.insert_trials()
        self.insert_recordings()
        end = time.time()
        print(f"Executia a durat {end - start} secunde")
