import sqlite3
import os
from typing import List
from data_access.models.input_model import InputModel
from data_access.models.new_input_model import NewInputModel
from data_access.models.new_recording import NewRecording
from data_access.models.recording import Recording
from data_access.models.trial import Trial
from data_access.models.user import User

import utils.database_constants as dbc
from utils.signal_constants import ALPHA_BAND_TYPE, BETA_BAND_TYPE, GAMMA_BAND_TYPE, BandType

class DataAccessService:

    db_connection: sqlite3.Connection

    def __init__(self) -> None:
        self.db_connection = sqlite3.connect(dbc.DATABASE_PATH)
        self.db_connection.execute(dbc.FOREIGN_KEYS_ENABLED)

    
    def initialize_database(self) -> None:
        """
        creates the tables in db
        """
        cursor = self.db_connection.cursor()
        cursor.execute(dbc.CREATE_USER_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_TRIAL_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_RECORDINGS_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_NEW_RECORDINGS_TABLE_SCRIPT)
        cursor.close()

    
    def insert_range_data(self, insert_script, entities) -> None:
        """
        inserts data in db
        """
        cursor = self.db_connection.cursor()
        entities_data = self.__get_entities_tuple(entities)
        cursor = cursor.executemany(insert_script, entities_data)
        self.db_connection.commit()
        cursor.close()

    
    def retrieve_range_data(self, select_script, entity_class) -> List:
        """
        retrieves data from db
            - inputs: sql select query, model type that needs to be extracted from the db
            - outputs: list of objects of entity_class type
        """
        cursor = self.db_connection.cursor()
        cursor.execute(select_script)
        entity_tuples = cursor.fetchall()
        return list(map(lambda entity_tuple: entity_class.from_entity_tuple(entity_tuple), entity_tuples))

   
    def clear_database(self) -> None:
        """
        closes the db connection and deletes the db file
        """
        self.db_connection.close()
        os.remove(dbc.DATABASE_PATH)

    def generate_input_models(self) -> List:
        """
        generates InputModel objects using the data from db
            - inputs: None
            - outputs: list of objects of InputModel type
        """
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

    def generate_new_input_models(self) -> List:
        """
        generates NewInputModel objects using the data from db
            - inputs: None
            - outputs: list of objects of NewInputModel type
        """
        users = self.retrieve_range_data(dbc.SELECT_USERS, User)
        trials = self.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
        recordings = self.retrieve_range_data(dbc.SELECT_NEW_RECORDINGS, NewRecording)
        input_models: List[NewInputModel] = []

        for user in users:
            for trial in trials:
                trial_outcome = "happy" if trial.quadrant == 1 else "sad"
                input_model_recordings: List[NewRecording] = list(filter(lambda rec: rec.trial_id == trial.trial_id and rec.user_id == user.user_id, recordings))
                input_model = NewInputModel(input_model_recordings, trial_outcome)
                input_models.append(input_model)
        return input_models

    def __get_entities_tuple(self, entities) -> List:
        """
        returns a list of tuples for the given entities
            - inputs: list of entities 
            - outputs: list of tuples
        """
        return list(map(lambda x: x.get_tuple(), entities))
