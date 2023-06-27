import matplotlib.pyplot as plt
import numpy as np

import utils.signal_constants as constants


def plot_signal(filtered_signal) -> None:
    plt.rcParams["figure.figsize"] = [15, 7]
    plt.rcParams["figure.autolayout"] = True
    t = np.arange(0, constants.SAMPLING_HIGHER_BOUND -
                  constants.SAMPLING_LOWER_BOUND)
    _, axs = plt.subplots()
    #axs.set_title("Signal")
    axs.plot(t, filtered_signal, color='b')
    #axs.set_xlabel("Time")
    #axs.set_ylabel("Amplitude")
    plt.show()


if __name__ == "__main__":
    plot_signal()
