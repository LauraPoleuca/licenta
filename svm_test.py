import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt

from data_access.data_access_service import DataAccessService

data_access = DataAccessService()
input_models = data_access.generate_input_models()[::3]
feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
# feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_sublist(), input_models)))
outcomes = np.array(list(map(lambda input_model: input_model.outcome, input_models)))

clf = svm.SVC(kernel = "rbf", gamma = 0.9999)
# clf = svm.SVC()
asd = clf.fit(feature_lists, outcomes)

fig = plt.figure()
ax = fig.add_subplot(projection = '3d')


predictions = clf.predict(feature_lists)
correct_count = len(list(filter(lambda i: predictions[i] == outcomes[i], range(len(predictions)))))
happy_count = len(list(filter(lambda o: o == "happy", outcomes)))
print(f"{correct_count / len(input_models)}% accuracy")
print(happy_count / len(input_models))


for input_model in input_models:
    point = input_model.get_feature_sublist()
    color = 'red' if input_model.outcome == "happy" else 'blue'
    ax.scatter(point[0], point[1], point[2], c=color)


ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()