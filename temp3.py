import matplotlib.pyplot as plt
import numpy as np

# Define the 5 entities and their attributes
entities = ['SVM', 'NN', 'K-means', 'GNB', 'NBC'][::-1]
attributes = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Balanced Accuracy'][::-1]

# Create random data (replace with your actual data)
data = np.random.rand(len(entities), len(attributes))
data = [
    [0.82, 0.82, 1, 0.9, 0.5][::-1],
    [0.8, 0.84, 1, 0.77, 0.55][::-1],
    [0.81, 0.84, 1, 0.89, 0.57][::-1],
    [0.77, 0.84, 0.97, 0.86, 0.62][::-1],
    [0.76, 0.83, 0.88, 0.85, 0.66][::-1]][::-1]
data = np.array(data)
# Set the height of each bar
bar_height = 0.2

# Calculate the y-axis positions for each entity's bars with added spacing
spacing = 0.1  # Adjust this value for more spacing
y = np.arange(len(entities)) * (len(attributes) * (bar_height + spacing))

# Create a horizontal bar for each attribute for each entity
for i, attr in enumerate(attributes):
    plt.barh(y + i * bar_height, data[:, i], bar_height, label=attr)

# Labeling
plt.yticks(y + ((len(attributes) - 1) * bar_height + (len(attributes) - 1) * spacing) / 2, entities)
plt.title('Performantele modelelor de clasificare')

legend = plt.legend(fontsize='small')  # You can adjust 'small' to another size if needed
# legend.set_bbox_to_anchor((1.05, 1))
# plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
