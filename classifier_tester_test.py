from typing import List
from classifiers.classifier_tester import ClassifierTester
from classifiers.dependencies.discretizer import Discretizer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from classifiers.neural_network import NeuralNetwork
from classifiers.svm_classifier import SVMClassifier
from data_access.data_access_service import DataAccessService
from data_access.models.input_model import InputModel

svm_classifier = SVMClassifier()
nn_classifier = NeuralNetwork()

discretizer = Discretizer(10)
naive_bayes_classifier = NaiveBayesClassifier(["ae", "se", "psd", "rms", "corr"], ["happy", "sad"], discretizer)

classifiers = [svm_classifier, naive_bayes_classifier, nn_classifier]
classifier_tester = ClassifierTester()

data_access = DataAccessService()
input_models: List[InputModel] = data_access.generate_input_models()[::3]

classifier_tester.setup_tester(input_models)

#this can sometimes crash because the intervals are set up in such a way that the values did not get taken into account and the intervals are too small 
results = classifier_tester.test_classifiers(classifiers)
for key in results:
    print(key, results[key])