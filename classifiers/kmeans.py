from typing import List
import numpy as np

from sklearn.cluster import KMeans
from classifiers.base_classifier import Classifier
from data_access.models.input_model import InputModel


class KMeansClusterer(Classifier):

    def __init__(self) -> None:
        self.name = "Kmeans classifier"
        self.clf = KMeans(n_clusters = 2)

    def train_classifier(self, input_models: List[InputModel]) -> None:
        super().train_classifier(input_models)
        feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
        self.clf.fit(feature_lists)

    def predict(self, input_model: InputModel):
        #TODO: don't know exactly if this is how the kmeans should be used
        return "happy" if self.clf.predict([input_model.get_feature_list()])[0] == 0 else "sad"
