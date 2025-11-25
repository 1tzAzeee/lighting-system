import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import serial.tools.list_ports


serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM1"
serialInst.open()


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.zones = []
        self.currentZone = []
        self.initUI()
        self.connects()


    def initUI(self):
        uic.loadUi('assets/UI/mainWindow.ui', self)
        self.setFixedSize(800, 600)
        with open("../zones.txt", 'r', encoding='utf-8') as f:
            self.zones = [i.rstrip().split(': ') + [False] for i in f.readlines()]
            for i in range(len(self.zones)):
                self.zones[i].append(i)
        self.allListWidget.addItems([i[0] for i in self.zones])



    def connects(self):
        self.allListWidget.currentItemChanged.connect(self.on_item_changed)
        self.onButton.clicked.connect(self.zone_enable)
        self.offButton.clicked.connect(self.zone_disable)

    def on_item_changed(self, current, previous):
        zone = current.text()
        for i in self.zones:
            if i[0] == zone:
                self.currentZone = i
        self.nameLabel.setText(zone)
        self.onButton.setEnabled(not self.currentZone[-2])
        self.offButton.setEnabled(self.currentZone[-2])

    def zone_enable(self):
        self.currentZone[-2] = True
        self.onButton.setEnabled(False)
        self.offButton.setEnabled(True)
        self.onListWidget.addItem(self.currentZone[0])

    def zone_disable(self):
        self.currentZone[-2] = False
        self.onButton.setEnabled(True)
        self.offButton.setEnabled(False)
        for i in range(self.onListWidget.count()):
            if self.currentZone[0] == self.onListWidget.item(i).text():
                self.onListWidget.takeItem(i)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    app.exec()
    serialInst.close()