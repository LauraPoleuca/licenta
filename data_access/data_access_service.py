import sqlite3
import os
from typing import List
from data_access.models.input_model import InputModel
from data_access.models.recording import Recording
from data_access.models.trial import Trial

import utils.database_constants as dbc
from utils.signal_constants import ALPHA_BAND_TYPE, BETA_BAND_TYPE, GAMMA_BAND_TYPE, BandType

class DataAccessService:

    db_connection: sqlite3.Connection

    def __init__(self) -> None:
        self.db_connection = sqlite3.connect(dbc.DATABASE_PATH)
        self.db_connection.execute(dbc.FOREIGN_KEYS_ENABLED)

    """
    Description - creates the tables in db
    """
    def initialize_database(self) -> None:
        cursor = self.db_connection.cursor()
        cursor.execute(dbc.CREATE_USER_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_TRIAL_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_RECORDINGS_TABLE_SCRIPT)
        cursor.close()

    """
    inserts data in db
    """
    def insert_range_data(self, insert_script, entities) -> None:
        cursor = self.db_connection.cursor()
        entities_data = self.__get_entities_tuple(entities)
        cursor = cursor.executemany(insert_script, entities_data)
        self.db_connection.commit()
        cursor.close()

    """
    retrieves data from db
        - inputs: 
        - outputs: list of objects of model type
    """
    def retrieve_range_data(self, select_script, entity_class) -> List:
        cursor = self.db_connection.cursor()
        cursor.execute(select_script)
        entity_tuples = cursor.fetchall()
        return list(map(lambda entity_tuple: entity_class.from_entity_tuple(entity_tuple), entity_tuples))

    """
    closes the db connection and removes
    """
    def clear_database(self) -> None:
        self.db_connection.close()
        os.remove(dbc.DATABASE_PATH)

    def generate_input_models(self) -> List:
        recordings = self.retrieve_range_data(dbc.SELECT_RECORDINGS, Recording)
        trials = self.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
        trials: List[Trial] = list(filter(lambda trial: trial.quadrant in [1, 3], trials))
        input_models: List[InputModel] = []
        for trial in trials:
            trial_outcome = "happy" if trial.quadrant == 1 else "sad"
            associated_recordings: List[Recording] = list(filter(lambda rec: rec.trial_id == trial.trial_id and rec.user_id == trial.user_id, recordings))
            for recording in associated_recordings:
                input_models.append(InputModel.from_list(recording.alpha_wave_features, trial_outcome, ALPHA_BAND_TYPE))
                input_models.append(InputModel.from_list(recording.beta_wave_features, trial_outcome, BETA_BAND_TYPE))
                input_models.append(InputModel.from_list(recording.gamma_wave_features, trial_outcome, GAMMA_BAND_TYPE))
        return input_models

    def __get_entities_tuple(self, entities) -> List:
        return list(map(lambda x: x.get_tuple(), entities))
