from typing import List

class ClassifierData:

    def __init__(self, classifier_name: str) -> None:
        self.test_evaluations: List = []
        self.true_positives: int = 0
        self.true_negatives: int = 0
        self.false_positives: int = 0
        self.false_negatives: int = 0
        self.classifier_name: str = classifier_name
    
    def calculate_metrics(self, expected_outcomes) -> List[float]:
        self.__reset_confusion_matrix()
        self.calculate_confusion_matrix(expected_outcomes)
        return [
            self.__calculate_accuracy(),
            self.__calculate_precision(),
            self.__calculate_recall(),
            self.__calculate_F1_score(),
            self.__calculate_balanced_accuracy()
        ]
    
    def calculate_confusion_matrix(self, expected_outcomes: List[str]):
        for index in range(len(expected_outcomes)):
            if expected_outcomes[index] == self.test_evaluations[index]:
                if self.test_evaluations[index] == "happy":
                    self.true_positives += 1
                else:
                    self.true_negatives += 1
            else:
                if self.test_evaluations[index] == "happy":
                    self.false_positives += 1
                else:
                    self.false_negatives += 1

    def __calculate_accuracy(self) -> float:
        return (self.true_positives + self.true_negatives) / (len(self.test_evaluations))
    
    def __calculate_precision(self) -> float:
        return (self.true_positives) / (self.true_positives + self.false_positives)
    
    def __calculate_recall(self) -> float:
        return self.true_positives / (self.true_positives + self.false_negatives)
    
    def __calculate_F1_score(self) -> float:
        precision = self.__calculate_precision()
        recall = self.__calculate_recall()
        return 2 * (precision * recall) / (precision + recall)
    
    def __calculate_specificity(self) -> float:
        return self.true_negatives / (self.true_negatives + self.false_positives)
    
    def __calculate_balanced_accuracy(self) -> float:
        recall = self.__calculate_recall()
        specificity = self.__calculate_specificity()
        return (recall + specificity) / 2
    
    def __reset_confusion_matrix(self):
        self.false_negatives = 0
        self.false_positives = 0
        self.true_negatives = 0
        self.true_positives = 0