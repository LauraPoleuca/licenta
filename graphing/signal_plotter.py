import matplotlib.pyplot as plt
import numpy as np

import utils.signal_constants as constants


def plot_signal(filtered_signal, band_type, user_name, trial_number, channel_name) -> None:
    plt.rcParams["figure.figsize"] = [15, 7]
    plt.rcParams["figure.autolayout"] = True
    t = np.arange(0, constants.SAMPLING_HIGHER_BOUND -
                  constants.SAMPLING_LOWER_BOUND)
    _, axs = plt.subplots()
    axs.set_title(
        f"Semnal filtrat pe banda {band_type.name.capitalize()} pentru subiectul {user_name}, trial {trial_number}, canal {channel_name}")
    sampled_filtered_signal = filtered_signal[constants.SAMPLING_LOWER_BOUND:constants.SAMPLING_HIGHER_BOUND]
    axs.plot(t, sampled_filtered_signal, color='b')
    ticks, labels = get_x_ticks(constants.SAMPLING_LOWER_BOUND, constants.SAMPLING_HIGHER_BOUND)
    plt.xticks(ticks, labels=labels)
    axs.set_xlabel("Timp (s)")
    axs.set_ylabel("Amplitudine semnal EEG (µV)")
    plt.show()


def plot_comparison(names, filtered_signals):
    plt.rcParams["figure.figsize"] = [15, 7]
    plt.rcParams["figure.autolayout"] = True
    t = np.arange(0, constants.SAMPLING_HIGHER_BOUND // 2 -
                  constants.SAMPLING_LOWER_BOUND // 2)
    _, axs = plt.subplots()
    axs.set_title(f"Comparatie pentru rezultatele filtrarii semnalelor")
    ticks, labels = get_x_ticks(constants.SAMPLING_LOWER_BOUND // 2, constants.SAMPLING_HIGHER_BOUND // 2)
    plt.xticks(ticks, labels=labels)

    for index in range(len(names)):
        sampled_filtered_signal = filtered_signals[index][
            constants.SAMPLING_LOWER_BOUND // 2: constants.SAMPLING_HIGHER_BOUND // 2]
        axs.plot(t, sampled_filtered_signal, label=names[index])
    axs.legend(names)
    axs.set_xlabel("Timp (s)")
    axs.set_ylabel("Amplitudine semnal EEG (µV)")
    plt.show()


def get_x_ticks(low, high):
    length = high - low
    ticks = []
    labels = []
    for index in range(length // constants.SAMPLING_RATE):
        ticks.append(index * constants.SAMPLING_RATE)
        labels.append(index)
    ticks.append(length)
    labels.append(length // constants.SAMPLING_RATE)
    return ticks, labels
