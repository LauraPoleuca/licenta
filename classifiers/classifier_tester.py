from typing import List
from sklearn.model_selection import train_test_split
from classifiers.base_classifier import Classifier
from classifiers.dependencies.classifier_data import ClassifierData
from data_access.models.input_model import InputModel


class ClassifierTester:

    # this class should let me do the comparisons
    def __init__(self) -> None:
        self.classifier_data_dict: dict = {}
        self.train_data: List[InputModel] = []
        self.test_data: List[InputModel] = []
        self.expected_outcomes: List[str] = []

    def setup_tester(self, input_models: List[InputModel], random_state=42):
        self.train_data, self.test_data = train_test_split(input_models, test_size=0.2, random_state=random_state)
        # self.train_data, self.test_data = np.split(input_models, [int(0.8 * len(input_models))])
        self.train_data = list(self.train_data)
        self.test_data = list(self.test_data)
        self.expected_outcomes = list(map(lambda input_model: input_model.outcome, self.test_data))

    def get_classifiers_results(self, classifiers: List[Classifier]) -> dict:
        self.train_classifiers(classifiers)
        self.fill_classifier_evaluations(classifiers)
        results = {}
        for classifier_name in self.classifier_data_dict:
            results[classifier_name] = self.classifier_data_dict[classifier_name].calculate_metrics(
                self.expected_outcomes)
        return results

    def train_classifiers(self, classifiers: List[Classifier]):
        for classifier in classifiers:
            classifier.train_classifier(self.train_data)

    def fill_classifier_evaluations(self, classifiers: List[Classifier]):
        """
        Sets up a classifier - classifier data dictionary.
        The ClassifierData object currently hold only a list of "test_evaluations"
        """
        self.classifier_data_dict = {}
        for classifier in classifiers:
            classifier_data: ClassifierData = ClassifierData(classifier.name)
            for input_model in self.test_data:
                predicition = classifier.predict(input_model)
                classifier_data.test_evaluations.append(predicition)
            self.classifier_data_dict[classifier.name] = classifier_data
