from copy import deepcopy
import json
from typing import List

import numpy as np
from classifiers.base_classifier import Classifier

from classifiers.dependencies.discretizer import Discretizer
from data_access.models.input_model import InputModel
from utils.data_extraction_constants import TRAINED_MODEL_FILE


class NaiveBayesClassifier(Classifier):

    def __init__(self, features: List[str], classes: List[str], discretizer: Discretizer) -> None:
        super().__init__()
        self.name = "Naive Bayes classifier"
        self.features: List[str] = features
        self.classes: List[str] = classes
        self.discretizer: Discretizer = discretizer
        self.train_data: dict = {}
        self.intervals: dict = {}

    def train_classifier(self, input_models: List[InputModel]) -> None:
        """
        Create a new frequency dictionary for all the features.
        For each data input in the dataset, pick up each of the features, determine the appropriate indexes for the bin
        and the class, and increase that. 
        Save this to the train_data property
        """
        self.train_data = self.__initialize_frequency_dict()
        self.intervals = self.__get_dataset_features_intervals(input_models)
        for data in input_models:
            # happy index 0, sad index 1
            class_index = self.__get_classification_index(data.outcome)
            for feature_name in self.features:
                feature_interval = self.intervals[feature_name]
                feature_value = data.__dict__[feature_name]
                bin_index = self.discretizer.get_bin_index(
                    feature_interval[0], feature_interval[1], feature_value)
                self.train_data[feature_name][class_index, bin_index] += 1
        # return self.train_data

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
            json.dump(serializable_model, file, indent = 4)

    def read_trained_model(self, filename: str = TRAINED_MODEL_FILE) -> None:
        with open(filename, 'r') as file:
            serialized_model = json.load(file)
            for feature in serialized_model:
                self.train_data[feature] = np.array([np.array(values_list)
                                                    for values_list in serialized_model[feature]])
        print(self.train_data)


    def __get_classification_index(self, class_name: str) -> int:
        return 0 if class_name == "happy" else 1

    def __get_class_likelyhood(self, features_model: InputModel, class_name: str) -> float:
        """
        Calculates the likelyhood of a given class to occur for a given features model.
        Based on the independency of the variables, this can be calculated as the product of
        all probabilities of type 
            P(x|class) = number of cases in which x resulted in the class / number of times in which the class occurs
        NOTE: temporary, if the class did not occur in the dataset, the probability is zero. 
        """
        class_index = self.__get_classification_index(class_name)
        prob = 1.0
        for feature in self.features:
            class_likelyhood = np.sum(self.train_data[feature][class_index])
            feature_interval = self.intervals[feature]
            feature_value = features_model.__dict__[feature]
            bin_index = self.discretizer.get_bin_index(
                feature_interval[0], feature_interval[1], feature_value)
            if class_likelyhood == 0:
                return 0  # temp solution until using log
            # TEMPORARY SOLUTION, FIX THIS!!!!
            if bin_index > self.discretizer.bin_count:
                return 0
            prob *= (self.train_data[feature]
                     [class_index, bin_index]) / class_likelyhood
        return prob
    
    def __get_dataset_features_intervals(self, dataset: List[InputModel]) -> dict:
        """
        Make a dict with all of the self.features as names and the intervals (currently as tuples)
        NOTE: this only works IF the features are set accordingly. Maybe there is a simpler implementation
        but this will do for now.
        """
        intervals: dict = {}
        # for gods sake please make sure you set the self.features correctly
        for feature_name in self.features:
            feature_values: List[float] = list(
                map(lambda data: data.__dict__[feature_name], dataset))
            intervals[feature_name] = (
                np.min(feature_values), np.max(feature_values))
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