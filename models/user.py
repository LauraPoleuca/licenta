from models.base_model import BaseModel

class User(BaseModel):

    def __init__(self, user_id: str, gender: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.gender = gender

    def get_tuple(self) -> tuple:
        return (self.user_id, self.gender)