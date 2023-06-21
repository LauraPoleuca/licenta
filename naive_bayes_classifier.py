import json
import numpy as np

from typing import List
from copy import deepcopy
from input_model_test import InputModel

from discretizer import Discretizer
from utils.data_extraction_constants import TRAINED_MODEL_FILE


class NaiveBayesClassifier:
    # data, which should be of type features & outcome
    # n features
    # into k classes

    # a method that takes a record and determines the likelyhood for each class
    # the likelyhood of each class is determined (in the end) as the probability of each feature given the class * the probability of the class

    # a private method that builds the frequency table for each feature given the dataset.
    # once all freq tables are built, do what?
    # this is essentially training, right?

    # a method that given the likelyhood of classes, picks a class (decision rule)

    def __init__(self, features: List[str], classes: List[str], discretizer: Discretizer) -> None:
        self.features: List[str] = features
        self.classes: List[str] = classes
        self.discretizer: Discretizer = discretizer
        self.train_data: dict = {}
        self.intervals: dict = {}

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

    def train_model(self, dataset: List[InputModel]) -> dict:
        """
        Create a new frequency dictionary for all the features.
        For each data input in the dataset, pick up each of the features, determine the appropriate indexes for the bin
        and the class, and increase that. 
        Save this to the train_data property
        """
        self.train_data = self.__initialize_frequency_dict()
        self.intervals = self.__get_dataset_features_intervals(dataset)
        for data in dataset:
            # happy index 0, sad index 1
            class_index = self.__get_classification_index(data.outcome)
            for feature_name in self.features:
                feature_interval = self.intervals[feature_name]
                feature_value = data.__dict__[feature_name]
                bin_index = self.discretizer.get_bin_index(
                    feature_interval[0], feature_interval[1], feature_value)
                self.train_data[feature_name][class_index, bin_index] += 1
        return self.train_data

    def __get_classification_index(self, class_name: str):
        return 0 if class_name == "happy" else 1

    def __get_class_likelyhood(self, features_model: InputModel, class_name: str):
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
            prob *= (self.train_data[feature]
                     [class_index, bin_index]) / class_likelyhood
        return prob

    def get_prediction(self, features_model: InputModel):
        """
        Calculates all probabilities for all classes.
        Uses the pick method to select a class returns it
        """
        class_predictions = list(map(lambda class_name: self.__get_class_likelyhood(
            features_model, class_name), self.classes))
        best_class_index = class_predictions.index(max(class_predictions))
        return self.classes[best_class_index]

    def store_trained_model(self, filename: str = TRAINED_MODEL_FILE):
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

    def read_trained_model(self, filename: str = TRAINED_MODEL_FILE):
        with open(filename, 'r') as file:
            serialized_model = json.load(file)
            for feature in serialized_model:
                self.train_data[feature] = np.array([np.array(values_list)
                                                    for values_list in serialized_model[feature]])
        print(self.train_data)
