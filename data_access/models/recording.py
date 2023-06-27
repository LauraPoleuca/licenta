from typing import List
from data_access.models.base_model import BaseModel


class Recording(BaseModel):
    # TODO: change order for parameters in this constructor to match the logical order
    def __init__(self, channel_id: str, user_id: str, trial_id: int, alpha_wave_features: List[float],
                 beta_wave_features: List[float], gamma_wave_features: List[float]) -> None:
        self.channel_id: str = channel_id
        self.user_id: str = user_id
        self.trial_id: int = trial_id
        self.alpha_wave_features: List[float] = alpha_wave_features
        self.beta_wave_features: List[float] = beta_wave_features
        self.gamma_wave_features: List[float] = gamma_wave_features
        super().__init__()

    def get_tuple(self) -> tuple:
        """
        returns a tuple based on a Recording object
        """
        return (
            str(self.user_id),
            self.trial_id,
            str(self.channel_id),
            # str(self.alpha_wave_features[0]),
            # str(self.alpha_wave_features[1]),
            # str(self.alpha_wave_features[2]),
            # str(self.alpha_wave_features[3]),
            # str(self.alpha_wave_features[4]),
            # str(self.beta_wave_features[0]),
            # str(self.beta_wave_features[1]),
            # str(self.beta_wave_features[2]),
            # str(self.beta_wave_features[3]),
            # str(self.beta_wave_features[4]),
            # str(self.gamma_wave_features[0]),
            # str(self.gamma_wave_features[1]),
            # str(self.gamma_wave_features[2]),
            # str(self.gamma_wave_features[3]),
            # str(self.gamma_wave_features[4]),
            *self.alpha_wave_features,
            *self.beta_wave_features,
            *self.gamma_wave_features,
        )

    @classmethod
    def from_entity_tuple(cls, entity_tuple: tuple) -> None:
        """
        acts as a constructor for a Recording
            - input: tuple representing the object
            - output: object of Recording type
        """
        return cls(entity_tuple[2],
                   entity_tuple[0],
                   entity_tuple[1],
                   [float(entity_tuple[3]),
                   float(entity_tuple[4]),
                   float(entity_tuple[5]),
                   float(entity_tuple[6]),
                   float(entity_tuple[7])],
                   [float(entity_tuple[8]),
                   float(entity_tuple[9]),
                   float(entity_tuple[10]),
                   float(entity_tuple[11]),
                   float(entity_tuple[12])],
                   [float(entity_tuple[13]),
                   float(entity_tuple[14]),
                   float(entity_tuple[15]),
                   float(entity_tuple[16]),
                   float(entity_tuple[17])])
