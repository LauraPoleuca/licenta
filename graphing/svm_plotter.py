from typing import List

from matplotlib import pyplot as plt

from data_access.models.input_model import InputModel


def plot_input_models(input_models: List[InputModel]):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for input_model in input_models:
        # considering a 3 dimensional subset of the input model in order to plot on a 3d axis system
        point = input_model.get_feature_sublist()
        color = 'red' if input_model.outcome == "happy" else 'blue'
        ax.scatter(point[0], point[1], point[2], c=color)
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_zlabel('Feature 3')
    plt.show()
