from typing import List
import numpy as np

from sklearn.naive_bayes import GaussianNB
from classifiers.base_classifier import Classifier
from data_access.models.input_model import InputModel


class GaussianNaiveBayesClasssifier(Classifier):

    def __init__(self) -> None:
        self.name = "Gaussian Naive Bayes Classifier"
        self.clf = GaussianNB()

    def train_classifier(self, input_models: List[InputModel]) -> None:
        super().train_classifier(input_models)
        feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
        outcomes = np.array(list(map(lambda input_model: input_model.outcome, input_models)))
        self.clf.fit(feature_lists, outcomes)

    def predict(self, input_model: InputModel):
        return self.clf.predict([input_model.get_feature_list()])[0]
