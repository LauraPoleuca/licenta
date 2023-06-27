from typing import List
from data_access.models.input_model import InputModel


class Classifier:
    
    def __init__(self) -> None:
        self.name = "Base classifier"

    def train_classifier(self, input_models: List[InputModel]) -> None:
        pass

    def predict(self, input_model: InputModel):
        pass

    def export_trained_model(self):
        pass

    def import_trained_model(self):
        pass