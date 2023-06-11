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
        

        self.tabs.addTab(self.tab1, "Tab1")
        self.tabs.addTab(self.tab2, "Tab2")
        self.tabs.addTab(self.tab3, "Tab3")
        self.tabs.addTab(self.tab4, "Tab4")
        

        self.bttn1 = QPushButton("Graphing1")
        self.bttn1.setFixedWidth(100)
        self.bttn1.setFixedHeight(100)
        self.bttn1.clicked.connect(onclick)

        self.bttn2 = QPushButton("Graphing2")
        self.bttn2.setFixedWidth(100)
        self.bttn2.setFixedHeight(100)

        self.bttn3 = QPushButton("Graphing3")
        self.bttn3.setFixedWidth(100)
        self.bttn3.setFixedHeight(100)

        self.bttn4 = QPushButton("Graphing4")
        self.bttn4.setFixedWidth(100)
        self.bttn4.setFixedHeight(100)
       
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.bttn1)
        self.tab1.layout.addWidget(self.bttn2)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.bttn3)
        self.tab2.layout.addWidget(self.bttn4)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


def onclick():
    print("clicked")

if __name__ == '__main__':
   app = QApplication(argv)
   wnd = ApplicationWnd()
   exit(app.exec_())
   