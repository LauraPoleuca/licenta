from input_model_test import InputModel
from naive_bayes_classifier import NaiveBayesClassifier
from discretizer import Discretizer

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

classificator.train_model(dataset)
print(classificator.get_prediction(InputModel(1, 4, 1, 1, 1, "happy")))
