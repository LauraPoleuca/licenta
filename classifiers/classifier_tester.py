from typing import List
from sklearn.model_selection import train_test_split
from classifiers.base_classifier import Classifier
from classifiers.dependencies.classifier_data import ClassifierData
from data_access.models.input_model import InputModel


class ClassifierTester:

    # this class should let me do the comparisons i deserve. I should get the same dataset for a series
    # of classifiers and then let every classifier do its thing, store the results
    def __init__(self) -> None:
        self.classifier_data_dict: dict = {}
        self.train_data: List[InputModel] = []
        self.test_data: List[InputModel] = []
        self.expected_outcomes: List[str] = []

    def setup_tester(self, input_models: List[InputModel]):
        # model_features = list(map(lambda input_model: input_model.get_feature_list(), input_models))
        self.train_data, self.test_data = train_test_split(input_models, test_size=0.2)
        self.expected_outcomes = list(map(lambda input_model: input_model.outcome, self.test_data))

    def test_classifiers(self, classifiers: List[Classifier]):
        self.train_classifiers(classifiers)
        self.fill_classifier_data(classifiers)
        results = {}
        for classifier in classifiers:
            results[classifier.name] = self.get_classifier_accuracy(classifier.name)
        return results
        
    def train_classifiers(self, classifiers: List[Classifier]):
        for classifier in classifiers:
            classifier.train_classifier(self.train_data)

    def fill_classifier_data(self, classifiers: List[Classifier]):
        self.classifier_data_dict = {}
        for classifier in classifiers:
            classifier_data: ClassifierData = ClassifierData()
            for input_model in self.test_data:
                predicition = classifier.predict(input_model)
                classifier_data.test_evaulations.append(predicition)
            self.classifier_data_dict[classifier.name] = classifier_data

    def get_classifier_accuracy(self, classifier_id: str) -> float:
        classifier_data: ClassifierData = self.classifier_data_dict[classifier_id]
        correct_evaluations = 0
        for index in range(len(classifier_data.test_evaulations)):
            if self.expected_outcomes[index] == classifier_data.test_evaulations[index]:
                correct_evaluations += 1
        return correct_evaluations / len(self.expected_outcomes)
