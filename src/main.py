import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        uic.loadUi('assets/UI/mainWindow.ui', self)
        self.setFixedSize(800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    app.exec()