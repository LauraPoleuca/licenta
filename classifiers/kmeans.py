from typing import List
import numpy as np

from sklearn.cluster import KMeans
from classifiers.base_classifier import Classifier
from data_access.models.input_model import InputModel


class KMeansClusterer(Classifier):

    def __init__(self) -> None:
        self.name = "Kmeans clusterer"
        self.clf = KMeans(n_clusters=2, n_init='auto')
        self.majority = None

    def train_classifier(self, input_models: List[InputModel]) -> None:
        super().train_classifier(input_models)
        feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
        self.clf.fit(feature_lists)
        predictions = self.clf.predict(feature_lists)
        # Since K means is a clusterer, not a classifier, the resulted clusters are unlabeled.
        # In order to determine which cluster, we are using the idea that due to the bias of the dataset towards "happy" emotions,
        # most values will be clustered around the "happy" centeroid.
        if len(list(filter(lambda x: x == 0, predictions))) > len(feature_lists) / 2:
            self.majority = 0
        else:
            self.majority = 1

    def predict(self, input_model: InputModel):
        return "happy" if self.clf.predict([input_model.get_feature_list()])[0] == self.majority else "sad"
