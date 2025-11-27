import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
import serial.tools.list_ports
from datetime import datetime as dt

serialInst = serial.Serial()
serialInst.baudrate = 9600
ports = serial.tools.list_ports.comports()
temp = ports.copy()
p = False
while not p:
    temp = ports.copy()
    ports = serial.tools.list_ports.comports()
    print([i.description for i in ports])
    for i in ports:
        if "CH340" in i.description or "Arduino" in i.description:
            port = i
            serialInst.port = port.name
            p = True
serialInst.open()


class errorDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('assets/UI/dialog1.ui', self)
        self.setWindowTitle("Ошибка")


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.zones = []
        self.currentZone = []
        self.enabledZone = []
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
        self.lcdNumber.display(str(len(self.zones)))

    def connects(self):
        self.allListWidget.currentItemChanged.connect(self.on_item_changed)
        self.onButton.clicked.connect(self.zone_enable)
        self.offButton.clicked.connect(self.zone_disable)
        self.logSaveButton.triggered.connect(self.saveLog)

    def on_item_changed(self, current, previous):
        zone = current.text()
        for i in self.zones:
            if i[0] == zone:
                self.currentZone = i
        self.nameLabel.setText(zone)
        self.onButton.setEnabled(not self.currentZone[-2])
        self.offButton.setEnabled(self.currentZone[-2])

    def zone_enable(self):
        if not self.enabledZone:
            try:
                self.currentZone[-2] = True
                self.onButton.setEnabled(False)
                self.offButton.setEnabled(True)
                self.enabledZone = self.currentZone.copy()
                self.enZoneLabel.setText(self.enabledZone[0])
                self.logUpdate(self.currentZone, "on")
                serialInst.write(f"on {self.currentZone[-1]}".encode("utf-8"))
                print(f"on {self.currentZone[-1]}".encode("utf-8"))
            except Exception:
                pass
        else:
            dialog = errorDialog()
            result = dialog.exec()

    def zone_disable(self):
        self.currentZone[-2] = False
        self.onButton.setEnabled(True)
        self.offButton.setEnabled(False)
        self.enabledZone.clear()
        self.enZoneLabel.setText('')
        self.logUpdate(self.currentZone, "off")
        print(f"off {self.currentZone[-1]}".encode("utf-8"))
        serialInst.write(f"off {self.currentZone[-1]}".encode("utf-8"))

    def logUpdate(self, zone, stat):
        dnow = dt.now().strftime("%H:%M %d.%m.%Y")
        if stat == "on":
            self.logText.append(f"{dnow} {zone[0]} включена")
        elif stat == "off":
            self.logText.append(f"{dnow} {zone[0]} выключена")
        elif stat == "saveLog":
            self.logText.append(f"{dnow} Сохранён файл журнала")

    def saveLog(self):
        dnow = dt.now().strftime("%d%m%Y%H%M")
        with open(f"log{dnow}.txt", "w", encoding="utf-8") as f:
            data = self.logText.toPlainText().split('\n')
            for i in data:
                f.write(f"{i}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    app.exec()
    serialInst.close()
