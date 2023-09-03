class BaseModel:

    def __init__(self) -> None:
        pass

    def get_tuple(self) -> tuple:
        return ()

    @classmethod
    def from_entity_tuple(self, entity_tuple):
        pass
