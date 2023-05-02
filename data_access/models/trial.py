from data_access.models.base_model import BaseModel

class Trial(BaseModel):

    def __init__(self, user_id: str, trial_id: int, valence: float, arousal: float, quadrant: int) -> None:
        self.user_id = user_id
        self.trial_id = trial_id
        self.valence = valence
        self.arousal = arousal
        self.quadrant = quadrant
        super().__init__()

    def get_tuple(self) -> tuple:
        return (self.user_id, 
            str(self.trial_id),
            str(self.valence),
            str(self.arousal),
            str(self.quadrant))