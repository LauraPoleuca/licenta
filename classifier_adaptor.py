from typing import List
from data_access.data_access_service import DataAccessService
from data_access.models.user import User
from data_access.models.trial import Trial
from data_access.models.recording import Recording
from discretizer import Discretizer
from input_model_test import InputModel
from naive_bayes_classifier import NaiveBayesClassifier
import utils.database_constants as dbc

data_service = DataAccessService()
recordings = data_service.retrieve_range_data(dbc.SELECT_RECORDINGS, Recording)
trials = data_service.retrieve_range_data(dbc.SELECT_TRIALS, Trial)


# TODO: add to constants later
bin_count = 10
discretizer = Discretizer(bin_count)
classifier = NaiveBayesClassifier(["ae", "se", "psd", "rms", "corr"], ["happy", "sad"], discretizer)
# classifier.train_model()

trials: List[Trial] = list(filter(lambda trial: trial.quadrant in [1, 3], trials))
input_models: List[InputModel] = []
for trial in trials:
    trial_outcome = "happy" if trial.quadrant == 1 else "sad"
    associated_recordings: List[Recording] = list(filter(lambda rec: rec.trial_id == trial.trial_id, recordings))
    for recording in associated_recordings:
        input_models.append(InputModel.from_list(recording.alpha_wave_features, trial_outcome))
        input_models.append(InputModel.from_list(recording.beta_wave_features, trial_outcome))
        input_models.append(InputModel.from_list(recording.gamma_wave_features, trial_outcome))

dic = classifier.train_model(input_models)
print(dic)
