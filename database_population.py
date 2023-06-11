import os
import time
from raw_data_extraction.recordings_extraction import get_recordings_multiprocessing
from raw_data_extraction.trial_extraction import get_trials
import utils.database_constants as dbc
from raw_data_extraction.user_extraction import get_users
from data_access.data_access_service import DataAccessService


def insert_users(data_access_service: DataAccessService):
    users = get_users()
    data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_USERS, users)


def insert_trials(data_access_service: DataAccessService):
    trials = get_trials()
    data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_TRIALS, trials)


def insert_recordings(data_access_service: DataAccessService):
    recordings = get_recordings_multiprocessing(["Fp1"])
    data_access_service.insert_range_data(dbc.INSERT_RANGE_TABLE_RECORDINGS, recordings)


def main():
    start = time.time()
    os.remove(dbc.DATABASE_PATH)
    data_access_service = DataAccessService()
    data_access_service.initialize_database()
    insert_users(data_access_service)
    insert_trials(data_access_service)
    insert_recordings(data_access_service)
    end = time.time()
    print(f"Executia a durat {end - start} secunde")


if __name__ == "__main__":
    main()
    print("Database was populated successfully")
