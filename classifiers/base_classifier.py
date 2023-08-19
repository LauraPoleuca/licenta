from typing import List
from data_access.models.input_model import InputModel


class Classifier:

    def __init__(self) -> None:
        self.name = "Base classifier"

    def train_classifier(self, input_models: List[InputModel]) -> None:
        """
        trains the classifier based on the given InputModels
        """
        pass

    def predict(self, input_model: InputModel) -> str:
        """
        predicts the outcome of the given InputModel
        """
        pass

    # TODO: remove things below
    def export_trained_model(self):
        pass

    def import_trained_model(self):
        pass
