import sqlite3
import os

import utils.database_constants as dbc
from data_access.models.user import User


class DataAccessService:

    db_connection: sqlite3.Connection

    def __init__(self) -> None:
        self.db_connection = sqlite3.connect(dbc.DATABASE_PATH)
        self.db_connection.execute(dbc.FOREIGN_KEYS_ENABLED)

    def initialize_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute(dbc.CREATE_USER_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_TRIAL_TABLE_SCRIPT)
        cursor.execute(dbc.CREATE_RECORDINGS_TABLE_SCRIPT)
        cursor.close()

    def insert_range_data(self, insert_script, entities):
        cursor = self.db_connection.cursor()
        entities_data = self.__get_entities_tuple(entities)
        cursor = cursor.executemany(insert_script, entities_data)
        self.db_connection.commit()
        cursor.close()

    def retrieve_range_data(self, select_script, entity_class):
        cursor = self.db_connection.cursor()
        cursor.execute(select_script)
        entity_tuples = cursor.fetchall()
        return list(map(lambda entity_tuple: entity_class.from_entity_tuple(entity_tuple), entity_tuples))

    def clear_database(self):
        self.db_connection.close()
        os.remove(dbc.DATABASE_PATH)

    def __get_entities_tuple(self, entities):
        return list(map(lambda x: x.get_tuple(), entities))
