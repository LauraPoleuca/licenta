from classifiers.dependencies.discretizer import Discretizer
from classifiers.naive_bayes_classifier import NaiveBayesClassifier
from data_access.models.input_model import InputModel

discretizer = Discretizer(5)
classificator = NaiveBayesClassifier(["ae", "se", "psd", "rms", "corr"], [
    "happy", "sad"], discretizer)


dataset = [
    InputModel(1, 1, 1, 1, 1, "happy"),
    InputModel(2, 4, 2, 2, 2, "happy"),
    InputModel(3, 4, 3, 3, 3, "happy"),
    InputModel(4, 4, 4, 4, 4, "sad"),
    InputModel(6, 4, 5, 5, 5, "sad")
]

d = classificator.train_classifier(dataset)
print(classificator.predict(InputModel(1, 4, 1, 1, 1, "happy")))
