from data_access.models.base_model import BaseModel


class NewRecording(BaseModel):
    """
    Holds the information for a certain recording. This type of recording is identified by
    the user_id, trial_id, channel_id and band type (alpha or beta).
    This should be used when building the input model. 
    For a trial, there are channel_count x band_count NewRecording objects needed. (40 in this case)
    """

    def __init__(self, user_id: str, trial_id: int, channel_id: str, band_type, features) -> None:
        self.user_id: str = user_id
        self.trial_id: int = trial_id
        self.channel_id: str = channel_id
        self.band_type = band_type
        self.features: features

    def get_tuple(self) -> tuple:
        """
        returns a tuple based on a NewRecording object
        """
        return (self.user_id, self.trial_id, self.channel_id, self.band_type, *self.features)
