from copy import deepcopy
import json
from typing import List

import numpy as np
from classifiers.base_classifier import Classifier

from classifiers.dependencies.discretizer import Discretizer
from data_access.models.input_model import InputModel
from data_access.models.recording import Recording
from utils.data_extraction_constants import TRAINED_MODEL_FILE
from utils.signal_constants import CHANNEL_INDEXES


class NaiveBayesClassifier(Classifier):

    def __init__(self, features: List[str], classes: List[str], discretizer: Discretizer) -> None:
        super().__init__()
        self.name = "Naive Bayes classifier"
        self.features: List[str] = features
        self.classes: List[str] = classes
        self.discretizer: Discretizer = discretizer
        self.train_data: dict = {}
        self.intervals: dict = {}
        self.model_count: int = 0

    @classmethod
    def default(cls):
        """
        A constructor for the classifier with some default values
        """
        discretizer = Discretizer(10)
        feature_names = []
        for x in CHANNEL_INDEXES:
            for y in ["alpha", "beta"]:
                for z in ["ae", "se", "psd", "rms", "corr"]:
                    feature_names.append(f"{x}-{y}-{z}")
        return cls(feature_names, ["happy", "sad"], discretizer)

    def train_classifier(self, input_models: List[InputModel]) -> None:
        """
        Create a new frequency dictionary for all the features.
        For each data input in the dataset, pick up each of the features, determine the appropriate indexes for the bin
        and the class, and increase that. 
        Save this to the train_data property
        """
        self.train_data = self.__initialize_frequency_dict()
        self.intervals = self.__get_dataset_features_intervals(input_models)
        self.model_count = len(input_models)
        for data in input_models:
            # happy index 0, sad index 1
            class_index = self.__get_classification_index(data.outcome)
            for feature_name in self.features:
                args = feature_name.split("-")
                feature_interval = self.intervals[feature_name]
                recording: Recording = list(
                    filter(
                        lambda r: r.channel_id == args[0] and r.band_type == args[1],
                        data.recordings))[0]
                feature_value = recording.get_feature_value_by_name(args[2])
                bin_index = self.discretizer.get_bin_index(
                    feature_interval[0], feature_interval[1], feature_value)
                self.train_data[feature_name][class_index, bin_index] += 1

    def predict(self, input_model: InputModel) -> List:
        """
        Calculates all probabilities for all classes.
        Uses the pick method to select a class returns it
        """
        class_predictions = list(map(lambda class_name: self.__get_class_likelyhood(
            input_model, class_name), self.classes))
        best_class_index = class_predictions.index(max(class_predictions))
        return self.classes[best_class_index]

    def store_trained_model(self, filename: str = TRAINED_MODEL_FILE) -> None:
        # convert ndarrays into lists for serialization
        serializable_model = {}
        for feature in self.features:
            serializable_model[feature] = []
            for classification in self.classes:
                class_index = self.__get_classification_index(classification)
                arr = self.train_data[feature][class_index].tolist()
                serializable_model[feature].append(arr)
        with open(filename, 'w') as file:
            json.dump(serializable_model, file, indent=4)

    def read_trained_model(self, filename: str = TRAINED_MODEL_FILE) -> None:
        with open(filename, 'r') as file:
            serialized_model = json.load(file)
            for feature in serialized_model:
                self.train_data[feature] = np.array([np.array(values_list)
                                                    for values_list in serialized_model[feature]])

    def __get_classification_index(self, class_name: str) -> int:
        return 0 if class_name == "happy" else 1

    def __get_class_likelyhood(self, features_model: InputModel, ck: str) -> float:
        """
        Calculates the likelyhood of a given class to occur for a given features model.
        Based on the independency of the variables, this can be calculated as the product of
        all probabilities of type 
            P(x|class) = number of cases in which x resulted in the class / number of times in which the class occurs
        NOTE: temporary, if the class did not occur in the dataset, the probability is zero. 
        """
        class_index = self.__get_classification_index(ck)
        class_likelyhood = None
        prob = 1.0
        for feature in self.features:
            class_likelyhood = np.sum(self.train_data[feature][class_index])
            feature_interval = self.intervals[feature]
            args = feature.split("-")
            recording: Recording = list(
                filter(
                    lambda r: r.channel_id == args[0] and r.band_type == args[1],
                    features_model.recordings))[0]
            feature_value = recording.get_feature_value_by_name(args[2])
            bin_index = self.discretizer.get_bin_index(
                feature_interval[0], feature_interval[1], feature_value)
            if bin_index > self.discretizer.bin_count:
                return 0
            prob *= self.train_data[feature][class_index, bin_index] / class_likelyhood
        return prob * (class_likelyhood / self.model_count)

    def __get_dataset_features_intervals(self, dataset: List[InputModel]) -> dict:
        """
        Make a dict with all of the self.features as names and the intervals (currently as tuples)
        NOTE: this only works IF the features are set accordingly. Maybe there is a simpler implementation
        but this will do for now.
        """
        intervals: dict = {}
        for feature_name in self.features:
            args = feature_name.split("-")
            feature_values = []
            for input_model in dataset:
                recordings = input_model.recordings
                x: List[Recording] = list(filter(lambda r: r.channel_id == args[0]
                                          and r.band_type == args[1], recordings))
                x: Recording = x[0]
                feature_values.append(x.get_feature_value_by_name(args[2]))
            intervals[feature_name] = (np.min(feature_values), np.max(feature_values))
        return intervals

    def __initialize_feature_frequency_table(self) -> np.ndarray:
        """
        Initialize a frequency table for a feature, which is a 2d matrix with the number of classes and bins  
        """
        return np.zeros((len(self.classes), self.discretizer.bin_count)).astype(int)

    def __initialize_frequency_dict(self) -> dict:
        """
        Intitialize a frequency dict, in which we associate a (new) frequency table for each feature 
        """
        frequency_dict = {}
        freq_table = self.__initialize_feature_frequency_table()
        for feature in self.features:
            frequency_dict[feature] = (deepcopy(freq_table))
        return frequency_dict
