from models.base_model import BaseModel


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
            str(self.beta_wave_features[0]),
            str(self.beta_wave_features[1]),
            str(self.beta_wave_features[2]),
            str(self.beta_wave_features[3]),
            str(self.gamma_wave_features[0]),
            str(self.gamma_wave_features[1]),
            str(self.gamma_wave_features[2]),
            str(self.gamma_wave_features[3]),
            )