from typing import List
from classifiers.classifier_tester import ClassifierTester
from classifiers.dependencies.discretizer import Discretizer
from classifiers.gaussian_naive_bayes_classifier import GaussianNaiveBayesClasssifier
from classifiers.kmeans import KMeansClusterer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from classifiers.neural_network import NeuralNetwork
from classifiers.svm_classifier import SVMClassifier
from data_access.data_access_service import DataAccessService
from data_access.models.input_model import InputModel

svm_classifier = SVMClassifier()
nn_classifier = NeuralNetwork()
kmeans_classifier = KMeansClusterer()
gnb_classifier = GaussianNaiveBayesClasssifier()
#discretizer = Discretizer(10)
#nb_classifier = NaiveBayesClassifier(["ae", "se", "psd", "rms", "corr"], ["happy", "sad"], discretizer)

classifiers = [svm_classifier, nn_classifier, kmeans_classifier, gnb_classifier]
classifier_tester = ClassifierTester()

data_access = DataAccessService()
input_models: List[InputModel] = data_access.generate_new_input_models()

classifier_tester.setup_tester(input_models)

#this can sometimes crash because the intervals are set up in such a way that the values did not get taken into account and the intervals are too small 
# results = classifier_tester.test_classifiers(classifiers)
# for key in results:
#     print(key, results[key])

results = classifier_tester.get_classifiers_results(classifiers)
for key in results:
    print(key)
    print("\t Accuracy:", results[key][0])
    print("\t Precision:", results[key][1])
    print("\t Recall:", results[key][2])
    print("\t F1 score:", results[key][3])
    print("\t Balanced accuracy:", results[key][4])