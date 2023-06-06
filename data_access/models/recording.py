from data_access.models.base_model import BaseModel


class Recording(BaseModel):
    def __init__(self, channel_id: str, user_id: str, trial_id: int, alpha_wave_features: list, beta_wave_features: list, gamma_wave_features: list) -> None:
        self.channel_id = channel_id
        self.user_id = user_id
        self.trial_id = trial_id
        self.alpha_wave_features = alpha_wave_features
        self.beta_wave_features = beta_wave_features
        self.gamma_wave_features = gamma_wave_features
        super().__init__()

    def get_tuple(self) -> tuple:
        return (
            str(self.user_id),
            self.trial_id,
            str(self.channel_id),
            str(self.alpha_wave_features[0]),
            str(self.alpha_wave_features[1]),
            str(self.alpha_wave_features[2]),
            str(self.alpha_wave_features[3]),
            str(self.alpha_wave_features[4]),
            str(self.beta_wave_features[0]),
            str(self.beta_wave_features[1]),
            str(self.beta_wave_features[2]),
            str(self.beta_wave_features[3]),
            str(self.beta_wave_features[4]),
            str(self.gamma_wave_features[0]),
            str(self.gamma_wave_features[1]),
            str(self.gamma_wave_features[2]),
            str(self.gamma_wave_features[3]),
            str(self.gamma_wave_features[4]),
        )

    @classmethod
    def from_entity_tuple(cls, entity_tuple: tuple) -> None:
        return cls(entity_tuple[0],
                   entity_tuple[1],
                   entity_tuple[2],
                   [entity_tuple[3],
                   entity_tuple[4],
                   entity_tuple[5],
                   entity_tuple[6],
                   entity_tuple[7]],
                   [entity_tuple[8],
                   entity_tuple[9],
                   entity_tuple[10],
                   entity_tuple[11],
                   entity_tuple[12]],
                   [entity_tuple[13],
                   entity_tuple[14],
                   entity_tuple[15],
                   entity_tuple[16],
                   entity_tuple[17]])
