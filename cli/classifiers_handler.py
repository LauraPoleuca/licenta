from typing import List

import tabulate
from halo import Halo

from business_logic.classifier_service import ClassifierService
from cli.cli_constants import TABLE_FORMAT
from data_access.data_access_service import DataAccessService
from data_access.models.input_model import InputModel


def handle_classifier_result():
    input_models = get_input_models()
    results = []
    with Halo(text="Antrenare..."):
        classifier_service = ClassifierService()
        results = classifier_service.test_all_classifiers(input_models)
    display_results(results)


@Halo(text="Generare modele pentru antrenare...")
def get_input_models():
    data_access = DataAccessService()
    input_models: List[InputModel] = data_access.generate_input_models()
    return input_models


def display_results(results):
    displayed_data = []
    for key in results:
        formatted_values = list(map(lambda v: f"{v * 100:.3f}%", results[key]))
        displayed_data.append([key] + formatted_values)
    print(tabulate.tabulate(
        displayed_data, headers=["Classifier", "Accuracy", "Precision", "Recall", "F1 score", "Balanced accuracy"],
        tablefmt=TABLE_FORMAT, colalign=("left", "right", "right", "right", "right", "right")))
