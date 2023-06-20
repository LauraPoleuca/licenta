from typing import List
from data_access.data_access_service import DataAccessService
from discretizer import Discretizer
from naive_bayes_classifier import NaiveBayesClassifier

data_service = DataAccessService()

# TODO: add to constants later
bin_count = 10
discretizer = Discretizer(bin_count)
classifier = NaiveBayesClassifier(["ae", "se", "psd", "rms", "corr"], ["happy", "sad"], discretizer)
if True:
    input_models = data_service.generate_input_models()
    dic = classifier.train_model(input_models)
    print(dic)
    classifier.store_trained_model()
else:
    classifier.read_trained_model()
    # do stuff
