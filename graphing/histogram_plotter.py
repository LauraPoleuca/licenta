import matplotlib.pyplot as plt


def plot_histograms(channel, feature, band, histogram_values, feature_interval):
    ticks = list(range(10))
    labels = []
    interval_length = (feature_interval[1] - feature_interval[0]) / 10
    for index in range(10):
        low_bound = f"{feature_interval[0] + index * interval_length: .3f}"
        high_bound = f"{feature_interval[0] + (index + 1) * interval_length :.3f}"
        labels.append(f"({low_bound}, {high_bound})")

    happy_data = histogram_values[0]
    sad_data = histogram_values[1]
    plt.figure(figsize=(16, 9))

    max_value = max(max(happy_data), max(sad_data)) + 5
    subplot_histogram(ticks, labels, happy_data, max_value, True)
    subplot_histogram(ticks, labels, sad_data, max_value, False)

    plt.suptitle(f'Histograms of the {feature} measured for channel {channel} ({band} banded signal)')
    plt.show()


def subplot_histogram(ticks, labels, values, max_value, is_happy):
    plt.subplot(1, 2, 1 if is_happy else 2)
    plt.bar(ticks, values, color='blue' if is_happy else 'pink')
    plt.xticks(ticks, labels=labels)

    curve_x = range(len(values))
    curve_y = values
    plt.plot(curve_x, curve_y, marker='o', color='red')
    plt.xlabel('Intervals')
    plt.ylabel('Data count')
    plt.title('Happy data histogram' if is_happy else 'Sad data histogram')
    plt.xticks(rotation=30)
    plt.ylim(0, max_value)  # Set y-axis limits
