import raw_data_extraction.data_extraction_helper as helper
from utils.data_extraction_constants import LABELS
from data_access.models.trial import Trial


def get_trials():
    files = helper.get_user_input_files()
    return sum(map(lambda file_name: get_user_trials(file_name), files), [])


def get_user_trials(file_name: str):
    file_content = helper.read_binary_file(file_name)
    username = helper.get_username_from_file(file_name)
    labels = file_content[LABELS]
    return list(map(lambda trial_index, label_set: Trial(username, trial_index + 1, label_set[0], label_set[1], get_user_trial_quadrant(label_set[0], label_set[1])), range(len(labels)), labels))


def get_user_trial_quadrant(valence: float, arousal: float):
    threshold_value = 4.5
    is_valence_high = valence > threshold_value
    is_arousal_high = arousal > threshold_value
    if is_valence_high and is_valence_high:
        return 1
    if not is_valence_high and is_arousal_high:
        return 2
    if not is_valence_high and not is_arousal_high:
        return 3
    return 4