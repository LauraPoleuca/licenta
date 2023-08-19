from typing import List
import numpy as np
from sklearn.neural_network import MLPClassifier
from classifiers.base_classifier import Classifier
from data_access.models.input_model import InputModel


class NeuralNetwork(Classifier):

    def __init__(self) -> None:
        self.name = "Neural Network"
        # TODO: set random_state for reproductability
        self.clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(5, 5), random_state=42, max_iter=2000)

    def train_classifier(self, input_models: List[InputModel]) -> None:
        super().train_classifier(input_models)
        feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
        outcomes = np.array(list(map(lambda input_model: input_model.outcome, input_models)))
        self.clf.fit(feature_lists, outcomes)

    def predict(self, input_model: InputModel):
        return self.clf.predict([input_model.get_feature_list()])[0]
