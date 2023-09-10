import sqlite3
import os
from typing import List, Tuple
from data_access.models.base_model import BaseModel
from data_access.models.input_model import InputModel
from data_access.models.recording import Recording
from data_access.models.trial import Trial
import utils.database_constants as dbc


class DataAccessService:

    db_connection: sqlite3.Connection

    def __init__(self) -> None:
        """
        Connects to the database file and enables the foreign keys constraints
        """
        self.db_connection = sqlite3.connect(dbc.DATABASE_PATH)
        self.db_connection.execute(dbc.FOREIGN_KEYS_ENABLED)

    def initialize_database(self) -> None:
        """
        Creates the tables in the database
        """
        cursor = self.db_connection.cursor()
        cursor.execute(dbc.CREATE_USER_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_TRIAL_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_RECORDINGS_TABLE_SCRIPT)
        cursor.close()

    def insert_range_data(self, insert_script, entities) -> None:
        """
        Inserts the given entities in the database using by executing the given insert script
        """
        cursor = self.db_connection.cursor()
        entities_data = self.__get_entities_tuple(entities)
        cursor = cursor.executemany(insert_script, entities_data)
        self.db_connection.commit()
        cursor.close()

    def retrieve_range_data(self, select_script, entity_class) -> List:
        """
        Executes the given select script and maps the returned results into the entity_class objects
        """
        cursor = self.db_connection.cursor()
        cursor.execute(select_script)
        entity_tuples = cursor.fetchall()
        return self.__get_entities_from_tuples(entity_tuples, entity_class)

    def clear_database(self) -> None:
        """
        closes the db connection and deletes the db file
        """
        self.db_connection.close()
        os.remove(dbc.DATABASE_PATH)

    def generate_input_models(self) -> List:
        """
        Generates InputModel objects using the data from db
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

    def __get_entities_tuple(self, entities: List[BaseModel]) -> List[Tuple]:
        """
        Returns a list of tuples for the given entities
        """
        return list(map(lambda x: x.get_tuple(), entities))

    def __get_entities_from_tuples(self, entity_tuples: List[Tuple], entity_class) -> List[BaseModel]:
        """
        Returns a list of entities of type entity_class from the given list of tuples 
        """
        return list(map(lambda entity_tuple: entity_class.from_entity_tuple(entity_tuple), entity_tuples))
