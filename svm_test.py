import numpy as np
from sklearn import svm
from sklearn import svc

from data_access.data_access_service import DataAccessService

# X = [[0, 0], [1, 1]]
# y = [0, 1]
# clf = svm.SVC()
# clf.fit(X, y)



# print(clf.predict([[2., 2.]]))

data_access = DataAccessService()
input_models = data_access.generate_input_models()
asd = list(map(lambda input_model: input_model.get_feature_list(), input_models))
feature_lists = np.array(list(map(lambda input_model: input_model.get_feature_list(), input_models)))
outcomes = np.array(list(map(lambda input_model: input_model.outcome, input_models)))

clf = svm.SVC()
asd = clf.fit(feature_lists, outcomes)

for input_model in input_models:
    prediction = clf.predict([input_model.get_feature_list()])
    print(prediction)
    # print(input_model.outcome == prediction)

print("ads")