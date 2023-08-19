from typing import List
import inquirer
import tabulate

from cli.cli_constants import TABLE_FORMAT, DatabasePreviewOptions
from data_access.data_access_service import DataAccessService
from data_access.models.recording import Recording
from data_access.models.trial import Trial
from data_access.models.user import User

import utils.database_constants as dbc


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
    data_access_service = DataAccessService()
    users = data_access_service.retrieve_range_data(dbc.SELECT_USERS, User)
    user_list = list(map(lambda u: list(u.get_tuple()), users))
    print(tabulate.tabulate(user_list, headers=["User id", "Gender"], tablefmt=TABLE_FORMAT))


def handle_preview_trials():
    data_access_service = DataAccessService()
    trials = data_access_service.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
    trials.sort(key=lambda t: (t.user_id, t.trial_id))
    trials_list = list(map(lambda t: list(t.get_tuple()), trials))
    print(
        tabulate.tabulate(
            trials_list, headers=["User id", "Trial id", "Valence", "Arousal", "Quadrant"],
            tablefmt=TABLE_FORMAT))


def handle_preview_recordings():
    data_access_service = DataAccessService()
    recordings = data_access_service.retrieve_range_data(dbc.SELECT_RECORDINGS, Recording)
    recordings.sort(key=lambda r: (r.user_id, r.trial_id, r.channel_id, r.band_type))
    recordings_list = list(map(lambda r: list(r.get_tuple()), recordings))[:500]
    print(
        tabulate.tabulate(
            recordings_list,
            headers=["User id", "Trial id", "Channel id", "Band type", "Approx. entropy", "Sample entropy", "PSD",
                     "RMS", "Auto correlation"],
            tablefmt=TABLE_FORMAT))
