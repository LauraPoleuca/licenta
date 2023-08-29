from typing import List
import inquirer
from business_logic.csv_generation_service import CSVGenerationService
from business_logic.database_generation_service import DatabaseGenerationService

from cli.cli_constants import BooleanOptions, DataGenerationOptions
from data_access.data_access_service import DataAccessService
from raw_data_extraction.raw_data_processor import process_raw_data


def get_data_generation_options() -> List[str]:
    return [
        DataGenerationOptions.CSV_Generation,
        DataGenerationOptions.Database_Population
    ]


def handle_data_generation() -> None:
    option = inquirer.list_input("Option", choices=get_data_generation_options())
    match option:
        case DataGenerationOptions.CSV_Generation:
            handle_dat_to_csv_conversion()
        case DataGenerationOptions.Database_Population:
            handle_database_generation()


def handle_dat_to_csv_conversion():
    if get_permission("Are you sure? This will delete the already existent .csv user files"):
        CSVGenerationService().generate_csv_files()


def handle_database_generation():
    if get_permission("Are you sure? This will delete the already existent database"):
        DatabaseGenerationService().populate_database()


def get_permission(msg: str = "Are you sure?") -> True:
    option = inquirer.list_input(msg, choices=[BooleanOptions.Yes, BooleanOptions.No])
    return option == BooleanOptions.Yes