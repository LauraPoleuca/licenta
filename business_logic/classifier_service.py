from classifiers.classifier_tester import ClassifierTester
from classifiers.gaussian_naive_bayes_classifier import GaussianNaiveBayesClasssifier
from classifiers.kmeans import KMeansClusterer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from classifiers.neural_network import NeuralNetwork
from classifiers.svm_classifier import SVMClassifier


class ClassifierService:

    def test_all_classifiers(self, input_models):
        svm_classifier = SVMClassifier()
        nn_classifier = NeuralNetwork()
        kmeans_classifier = KMeansClusterer()
        gnb_classifier = GaussianNaiveBayesClasssifier()
        nb_classifier = NaiveBayesClassifier.default()
        classifiers = [svm_classifier, nn_classifier, kmeans_classifier, gnb_classifier, nb_classifier]

        classifier_tester = ClassifierTester()
        results = self.train_classifiers(classifier_tester, classifiers, input_models, 0)
        nb_classifier.store_trained_model()

        return results

    def train_classifiers(self, classifier_tester: ClassifierTester, classifiers, input_models, state):
        classifier_tester.setup_tester(input_models, random_state=state)
        results = classifier_tester.get_classifiers_results(classifiers)
        return results
