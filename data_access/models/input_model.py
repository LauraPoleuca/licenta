from typing import List

from data_access.models.recording import Recording


class InputModel:
    """
    Represents the new input model. It essentially contains all the recordings associated with a trial
    (one input model per user_id - trial_id), as well as the outcome of the trial. 
    There are 20 x 2 recordings expected per model 
    """

    def __init__(self, recordings: List[Recording], outcome: str) -> None:
        self.recordings: List[Recording] = recordings
        self.outcome: str = outcome

    def get_feature_list(self) -> List[float]:
        """
        Compiles all features from all recordings into a single list that can be used for the classification process
        """
        features: List[float] = []
        for rec in self.recordings:
            features += rec.features
        return features
