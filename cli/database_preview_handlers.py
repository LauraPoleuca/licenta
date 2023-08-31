from typing import List

import inquirer
import tabulate

from business_logic.data_extraction_service import DataExtractionService
from cli.cli_constants import TABLE_FORMAT, DatabasePreviewOptions


def get_database_preview_options() -> List[str]:
    return [
        DatabasePreviewOptions.Users,
        DatabasePreviewOptions.Trials,
        DatabasePreviewOptions.Recordings
    ]


def handle_database_preview():
    option = inquirer.list_input("Entity to preview", choices=get_database_preview_options())
    match option:
        case DatabasePreviewOptions.Users:
            handle_preview_users()
        case DatabasePreviewOptions.Trials:
            handle_preview_trials()
        case DatabasePreviewOptions.Recordings:
            handle_preview_recordings()


def handle_preview_users():
    user_tuple_list = DataExtractionService().extract_user_data()
    print(tabulate.tabulate(user_tuple_list, headers=["User id", "Gender"], tablefmt=TABLE_FORMAT))


def handle_preview_trials():
    trials_list = DataExtractionService().extract_trial_data()
    print(tabulate.tabulate(
        trials_list, headers=["User id", "Trial id", "Valence", "Arousal", "Quadrant"],
        tablefmt=TABLE_FORMAT))


def handle_preview_recordings():
    recordings_list = DataExtractionService().extract_recording_data()
    print(tabulate.tabulate(
        recordings_list,
        headers=["User id", "Trial id", "Channel id", "Band type", "Approx. entropy", "Sample entropy", "PSD",
                 "RMS", "Auto correlation"],
        tablefmt=TABLE_FORMAT))
