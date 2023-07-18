from typing import List
import numpy as np

from sklearn import svm
from classifiers.base_classifier import Classifier
from data_access.models.input_model import InputModel
from data_access.models.new_input_model import NewInputModel


class SVMClassifier(Classifier): 

    def __init__(self) -> None:
        super().__init__()
        self.name = "svm"
        self.clf = svm.SVC(kernel = "rbf", gamma = 0.9999)

    def train_classifier(self, input_models: List[NewInputModel]) -> None:
        super().train_classifier(input_models)
        feature_lists: List[List[float]] = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
        outcomes: List[str] = np.array(list(map(lambda input_model: input_model.outcome, input_models)))
        self.clf.fit(feature_lists, outcomes)
    
    def predict(self, input_model: NewInputModel):
        return self.clf.predict([input_model.get_feature_list()])[0]
        