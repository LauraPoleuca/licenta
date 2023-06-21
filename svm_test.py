import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt

from data_access.data_access_service import DataAccessService

# X = [[0, 0], [1, 1]]
# y = [0, 1]
# clf = svm.SVC()
# clf.fit(X, y)



# print(clf.predict([[2., 2.]]))

data_access = DataAccessService()
input_models = data_access.generate_input_models()[::3]
asd = list(map(lambda input_model: input_model.get_feature_list(), input_models))
# feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_sublist(), input_models)))
outcomes = np.array(list(map(lambda input_model: input_model.outcome, input_models)))

clf = svm.SVC(kernel="rbf", gamma=0.999)
# clf = svm.SVC(kernel="sigmoid")
asd = clf.fit(feature_lists, outcomes)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

x = 0
# for input_model in filter(lambda m: m.outcome == "sad", input_models):
for input_model in input_models:
    # prediction = clf.predict([input_model.get_feature_list()])
    point = input_model.get_feature_sublist()
    m = 'red' if input_model.outcome == "happy" else 'blue'
    ax.scatter(point[0], point[1], point[2], c=m)
    prediction = clf.predict([input_model.get_feature_sublist()])
    print(prediction[0] == input_model.outcome)
    if(prediction[0] == input_model.outcome):
        x += 1
    else:
        print
    # print(input_model.outcome == prediction)

print(x / len(input_models))
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()