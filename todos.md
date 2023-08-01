# Todos

## General

- [ ] Use classes for all unassigned methods (at least static ones)
- [ ] Add comments
- [X] Use typing in all methods
- [ ] Maybe set bin count to be specific per property, not per discretizer.
- [X] Create class index method instead of 0 else 1
- [X] Order methods in classes (private, protected, public)
- [X] Add multithreading / multiprocessing for the user files, add locks for data access
- [X] Since the program uses only trials with quadrant classification 1 or 3, don't create useless records and process data for nothing
- [ ] Make histograms for the training data for the relevant features in each state (happy / sad)
- [X] Add classifier adaptor content as data access method
- [X] Move input model class in models
- [ ] Check the naive classifier, I think P(Ck) is missing and should be calculated in order to be multiplied to the final product
- [ ] Switch to using logs when calculating probabilities in bayes, since a 0 value for a bin means a final 0 probaility

## UI

- [ ] Setups Tab: .dat -> .csv, database population
- [ ] Database preview
- [ ] Graphing Tab: signal bands, histograms
- [ ] Naive Bayes Classifier: train, predict
- [ ] SVM

## Input model transitioning

- [X] Create new models
- [ ] Create new scripts for adding and saving NewRecording in the database
- [ ] Add new method which builds the NewRecording objects and saves them in the database in database_population.py
- [ ] Adjust rest of the code (needs more elaboration)

## Classifier metrics
The app needs a way to record the actual classification results for each evaluation and each classifier. 
The evaluation results need to be accounted for not inside the classifier. 
It would be good to record the accuracy of the prediction as well for the NBC.
 - [ ] Add method to evaluate based on a list of input models, not only one model
 - [ ] Evaluate results into confusion matrix
 - [ ] Calculate stats within the ClassifierData object