import sqlite3
import os
from typing import List
from data_access.models.input_model import InputModel
from data_access.models.recording import Recording
from data_access.models.trial import Trial
import utils.database_constants as dbc


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
            - outputs: list of objects of entity_class type
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
            - outputs: list of objects of NewInputModel type
        """
        trials = self.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
        recordings = self.retrieve_range_data(dbc.SELECT_RECORDINGS, Recording)
        input_models: List[InputModel] = []

        for trial in trials:
            trial_outcome = "happy" if trial.quadrant == 1 else "sad"
            input_model_recordings: List[Recording] = list(
                filter(lambda rec: rec.trial_id == trial.trial_id and rec.user_id == trial.user_id, recordings))
            input_model = InputModel(input_model_recordings, trial_outcome)
            input_models.append(input_model)
        return input_models

    def __get_entities_tuple(self, entities) -> List:
        """
        returns a list of tuples for the given entities
            - inputs: list of entities 
            - outputs: list of tuples
        """
        return list(map(lambda x: x.get_tuple(), entities))
