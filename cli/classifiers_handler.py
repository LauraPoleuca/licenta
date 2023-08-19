from typing import List
import tabulate
import yaspin

from classifiers.classifier_tester import ClassifierTester
from classifiers.dependencies.discretizer import Discretizer
from classifiers.gaussian_naive_bayes_classifier import GaussianNaiveBayesClasssifier
from classifiers.kmeans import KMeansClusterer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from classifiers.neural_network import NeuralNetwork
from classifiers.svm_classifier import SVMClassifier
from cli.cli_constants import TABLE_FORMAT
from data_access.data_access_service import DataAccessService
from data_access.models.input_model import InputModel
from utils.signal_constants import CHANNEL_INDEXES


def handle_classifiers():
    svm_classifier = SVMClassifier()
    nn_classifier = NeuralNetwork()
    kmeans_classifier = KMeansClusterer()
    gnb_classifier = GaussianNaiveBayesClasssifier()

    input_models = get_input_models()
    for state in range(1000):
        print("state = ", state)
        discretizer = Discretizer(10)
        feature_names = []
        # ch1-alpha-ae, ch1-alpha-se, ..., ch1-beta-ae, ...
        for x in CHANNEL_INDEXES:
            for y in ["alpha", "beta"]:
                for z in ["ae", "se", "psd", "rms", "corr"]:
                    feature_names.append(f"{x}-{y}-{z}")
        nb_classifier = NaiveBayesClassifier(feature_names, ["happy", "sad"], discretizer)

        classifiers = [svm_classifier, nn_classifier, kmeans_classifier, gnb_classifier, nb_classifier]
        classifier_tester = ClassifierTester()
        results = train_classifiers(classifier_tester, classifiers, input_models, state)
        display_results(results)

    pass


@yaspin.yaspin(text="Generating input models...")
def get_input_models():
    data_access = DataAccessService()
    input_models: List[InputModel] = data_access.generate_input_models()
    return input_models


@yaspin.yaspin(text="Training...")
def train_classifiers(classifier_tester: ClassifierTester, classifiers, input_models, state):
    classifier_tester.setup_tester(input_models, random_state=state)
    results = classifier_tester.get_classifiers_results(classifiers)
    return results


def display_results(results):
    displayed_data = []
    for key in results:
        formatted_values = list(map(lambda v: f"{v * 100:.3f}%", results[key]))
        displayed_data.append([key] + formatted_values)
    print(
        tabulate.tabulate(
            displayed_data, headers=["Classifier", "Accuracy", "Precision", "Recall", "F1 score", "Balanced accuracy"],
            tablefmt=TABLE_FORMAT, colalign=("left", "right", "right", "right", "right", "right")))
