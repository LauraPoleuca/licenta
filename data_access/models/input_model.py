from typing import List

from data_access.models.recording import Recording


class InputModel:
    """
    Represents the new input model. It essentially contains all the recordings associated with a trial
    (one newInputModel per user_id-trial_id), as well as the outcome of the trial. There are 20 x 2 recordings expected
    in the current siutuation but maybe that will change. 
    """

    def __init__(self, recordings: List[Recording], outcome: str) -> None:
        self.recordings: List[Recording] = recordings
        self.outcome: str = outcome

    def get_feature_list(self) -> List[float]:
        """
        Compiles all the features from all recordings into a single list that can be used for the actual training of the classifiers
        """
        features: List[float] = []
        for rec in self.recordings:
            features += rec.features
        return features
