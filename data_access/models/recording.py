from typing import List
from data_access.models.base_model import BaseModel


class Recording(BaseModel):
    """
    Holds the information for a certain recording. This type of recording is identified by
    the user_id, trial_id, channel_id and band type (alpha or beta).
    This should be used when building the input model. 
    For a trial, there are channel_count x band_count NewRecording objects needed. (40 in this case)
    """

    def __init__(self, user_id: str, trial_id: int, channel_id: str, band_type: str, features: List[float]) -> None:
        self.user_id: str = user_id
        self.trial_id: int = trial_id
        self.channel_id: str = channel_id
        self.band_type: str = band_type
        self.features = features

    def get_tuple(self) -> tuple:
        """
        returns a tuple based on a Recording object
        """
        return (self.user_id, self.trial_id, self.channel_id, self.band_type, *self.features)

    @classmethod
    def from_entity_tuple(cls, entity_tuple: tuple) -> None:
        return cls(entity_tuple[0],
                   entity_tuple[1],
                   entity_tuple[2],
                   entity_tuple[3],
                   [float(entity_tuple[4]),
                   float(entity_tuple[5]),
                   float(entity_tuple[6]),
                   float(entity_tuple[7]),
                   float(entity_tuple[8])])
    
    # I don't like this but here we go
    def get_feature_value_by_name(self, name: str) -> float:
        index = -1
        if name == "ae":
            index = 0
        elif name == "se":
            index = 1
        elif name == "psd":
            index = 2
        elif name == "rms":
            index = 3
        elif name == "corr":
            index = 4
        return self.features[index]