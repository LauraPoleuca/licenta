from data_access.models.base_model import BaseModel

class User(BaseModel):

    def __init__(self, user_id: str, gender: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.gender = gender

    @classmethod
    def from_entity_tuple(cls, entity_tuple: tuple) -> None:
        return cls(entity_tuple[0], entity_tuple[1])

    def get_tuple(self) -> tuple:
        return (self.user_id, self.gender)