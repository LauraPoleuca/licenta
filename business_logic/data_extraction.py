from typing import List, Tuple

import utils.database_constants as dbc
from data_access.data_access_service import DataAccessService
from data_access.models.recording import Recording
from data_access.models.trial import Trial
from data_access.models.user import User


class DataExtractionService:

    def __init__(self) -> None:
        self.data_access_service = DataAccessService()

    def extract_user_data(self) -> List[Tuple]:
        users = self.data_access_service.retrieve_range_data(dbc.SELECT_USERS, User)
        user_tuple_list = list(map(lambda u: list(u.get_tuple()), users))
        return user_tuple_list

    def extract_trial_data(self) -> List[Tuple]:
        trials = self.data_access_service.retrieve_range_data(dbc.SELECT_TRIALS, Trial)
        trials.sort(key=lambda t: (t.user_id, t.trial_id))
        trial_tuple_list = list(map(lambda t: list(t.get_tuple()), trials))
        return trial_tuple_list

    def extract_recording_data(self) -> List[Tuple]:
        recordings = self.data_access_service.retrieve_range_data(dbc.SELECT_RECORDINGS, Recording)
        recordings.sort(key=lambda r: (r.user_id, r.trial_id, r.channel_id, r.band_type))
        recording_tuple_list = list(map(lambda r: list(r.get_tuple()), recordings))[:500]
        return recording_tuple_list
