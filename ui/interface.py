from sys import *
from PyQt5.QtWidgets import *

class ApplicationWnd(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("app")
        self.setGeometry(100, 100, 700, 450)
        self.t_widget = TWidget(self)
        self.setCentralWidget(self.t_widget)
        self.show()

class TWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        

        self.tabs.addTab(self.tab1, "Setups")
        self.tabs.addTab(self.tab2, "Database Preview")
        self.tabs.addTab(self.tab3, "Graphing")
        self.tabs.addTab(self.tab4, "Naive Bayes Classifier")
        self.tabs.addTab(self.tab5, "SVM")
        
        self.bttn1 = QPushButton(".dat -> .csv")
        self.bttn1.setFixedWidth(100)
        self.bttn1.setFixedHeight(100)

        self.bttn2 = QPushButton("Database Population")
        self.bttn2.setFixedWidth(200)
        self.bttn2.setFixedHeight(100)

        self.bttn3 = QPushButton("Signal Bands")
        self.bttn3.setFixedWidth(100)
        self.bttn3.setFixedHeight(100)
        self.bttn3.clicked.connect(self.sd)
    
        self.bttn4 = QPushButton("Histograms")
        self.bttn4.setFixedWidth(100)
        self.bttn4.setFixedHeight(100)

        self.bttn5 = QPushButton("Train")
        self.bttn5.setFixedWidth(100)
        self.bttn5.setFixedHeight(100)

        self.bttn6 = QPushButton("Predict")
        self.bttn6.setFixedWidth(100)
        self.bttn6.setFixedHeight(100)
        self.bttn3.clicked.connect(self.onclick)
       
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.bttn1)
        self.tab1.layout.addWidget(self.bttn2)
        self.tab1.setLayout(self.tab1.layout)

        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addWidget(self.bttn3)
        self.tab3.layout.addWidget(self.bttn4)
        self.tab3.setLayout(self.tab3.layout)

        self.tab4.layout = QVBoxLayout(self)
        self.tab4.layout.addWidget(self.bttn5)
        self.tab4.layout.addWidget(self.bttn6)
        self.tab4.setLayout(self.tab4.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def onclick(self):
        text, ok = QInputDialog.getText(self, ' ', 'Enter trial:')
        if ok:
            self.le.setText(str(text))

    def sd(self):
        dialog = InputDialog()
        dialog.setWindowTitle("Waves")
        if dialog.exec():
            print(dialog.getInputs())

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        self.third = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("User", self.first)
        layout.addRow("Trial", self.second)
        layout.addRow("WaveBand", self.third)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

if __name__ == '__main__':
   app = QApplication(argv)
   wnd = ApplicationWnd()
   exit(app.exec_())
   