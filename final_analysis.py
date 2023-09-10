import numpy as np
import tabulate
from classifiers.classifier_tester import ClassifierTester
from classifiers.gaussian_naive_bayes_classifier import GaussianNaiveBayesClasssifier
from classifiers.kmeans import KMeansClusterer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from classifiers.neural_network import NeuralNetwork
from classifiers.svm_classifier import SVMClassifier
from cli.cli_constants import TABLE_FORMAT
from data_access.data_access_service import DataAccessService


classifier_tester = ClassifierTester()
svm_classifier = SVMClassifier()
nn_classifier = NeuralNetwork()
kmeans_classifier = KMeansClusterer()
gnb_classifier = GaussianNaiveBayesClasssifier()
nb_classifier = NaiveBayesClassifier.default()
classifiers = [svm_classifier, nn_classifier, kmeans_classifier, gnb_classifier, nb_classifier]

input_models = DataAccessService().generate_input_models()
classification_results = {
    svm_classifier.name: [],
    nn_classifier.name: [],
    kmeans_classifier.name: [],
    gnb_classifier.name: [],
    nb_classifier.name: []
}

for state in range(1000):
    print(state)
    classifier_tester = ClassifierTester()
    svm_classifier = SVMClassifier()
    nn_classifier = NeuralNetwork()
    kmeans_classifier = KMeansClusterer()
    gnb_classifier = GaussianNaiveBayesClasssifier()
    nb_classifier = NaiveBayesClassifier.default()
    classifiers = [svm_classifier, nn_classifier, kmeans_classifier, gnb_classifier, nb_classifier]
    classifier_tester.setup_tester(input_models, random_state=state)
    results = classifier_tester.get_classifiers_results(classifiers)
    for key in results:
        classification_results[key].append(results[key])

metrics = ["Accuracy", "Precision", "Recall", "F1 score", "Balanced accuracy"]
displayed_data = []
best_displayed_data = []
worst_displayed_data = []
average_displayed_data = []
for classifier in classification_results:
    best = []
    worst = []
    avg = []
    for metric_index in range(5):
        # print(metrics[metric_index])
        metric_values = list(map(lambda lst: lst[metric_index], classification_results[classifier]))
        metric_low = min(metric_values)
        metric_high = max(metric_values)
        metric_avg = np.average(metric_values)
        displayed_data.append([classifier, metrics[metric_index], metric_high, metric_low, metric_avg])
        best.append(metric_high)
        worst.append(metric_low)
        avg.append(metric_avg)
    best_displayed_data.append([classifier] + best)
    worst_displayed_data.append([classifier] + worst)
    average_displayed_data.append([classifier] + avg)

# for classifier in classification_results:
#     best = []
#     for metric_index in range(5):
#         metric_values = list(map(lambda lst: lst[metric_index], classification_results[classifier]))
#         best.append

print("Best results:")
print(tabulate.tabulate(
    best_displayed_data, headers=["Classifier"] + metrics,
    tablefmt=TABLE_FORMAT, colalign=("left", "right", "right", "right", "right", "right")))

print("Worst results:")
print(tabulate.tabulate(
    worst_displayed_data, headers=["Classifier"] + metrics,
    tablefmt=TABLE_FORMAT, colalign=("left", "right", "right", "right", "right", "right")))

print("Average results:")
print(tabulate.tabulate(
    average_displayed_data, headers=["Classifier"] + metrics,
    tablefmt=TABLE_FORMAT, colalign=("left", "right", "right", "right", "right", "right")))

# print(tabulate.tabulate(
#     displayed_data, headers=["Classifier/Metric", "Metric", "Best", "Worst", "Average"],
#     tablefmt=TABLE_FORMAT, colalign=("left", "left", "right", "right", "right")))
