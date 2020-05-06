import sys
import os

import simplelogging

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget)

from UI_maindlg import Ui_Dialog

revision = 1.0

LOG_CONSOLE_FORMAT = "%(log_color)s%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):: %(message)s%(reset)s"
LOG_FILE_FORMAT = "%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):: %(message)s"
log = simplelogging.get_logger(file_format=LOG_FILE_FORMAT, console_format=LOG_CONSOLE_FORMAT, file_name='log.log')

class AppWindow(QMainWindow, Ui_Dialog):
    def center(self):
        framegm = self.frameGeometry()
        centrepoint = QDesktopWidget().availableGeometry().center()
        framegm.moveCenter(centrepoint)
        self.move(framegm.topLeft())

    def __init__(self):
        super(AppWindow, self).__init__()
        self.setupUi(self)
        self.show()
        self.center()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

        self.swSelection.setCurrentIndex(0)
        self.cbxCode.setVisible(False)
        self.resize(560, 320)

        self.LoadCountries()

        self.lwOptions.clicked.connect(self.OnListClick)
        self.pbClose.clicked.connect(self.OnCloseClick)
        self.cbViewTerminal.stateChanged.connect(self.OnViewTerminalChange)

        # Quick functions
        self.pbConnectQuick.clicked.connect(self.OnConnectQuickClick)
        self.pbDisconnectQuick.clicked.connect(self.OnDisconnectQuickClick)

        # Select from lists
        self.pbConnectList.clicked.connect(self.OnConnectListClick)
        self.pbDisconnectList.clicked.connect(self.OnDisconnectListClick)
        self.cbxCountry.currentTextChanged.connect(self.LoadCities)

        # Select by server code
        self.pbConnectCode.clicked.connect(self.OnConnectCodeClick)
        self.pbDisconnectCode.clicked.connect(self.OnDisconnectCodeClick)

    def LoadCountries(self):
        self.cbxCountry.clear()
        self.cbxCountry.addItem('Select Country')
        c = self.NordCommand('nordvpn countries')
        t = c.split('\n')
        countries = t[6].split(', ')
        self.cbxCountry.addItems(countries)

    def LoadCities(self):
        self.pbConnectList.setEnabled(True)
        self.cbxCity.clear()
        self.cbxCity.addItem('Select City')
        c = self.NordCommand('nordvpn cities {}'.format(self.cbxCountry.currentText()))
        t = c.split('\n')
        cities = t[6].split(', ')
        self.cbxCity.addItems(cities)

    def OnViewTerminalChange(self):
        if self.cbViewTerminal.isChecked():
            self.resize(560, 560)
        else:
            self.resize(560, 320)

    def OnCloseClick(self):
        QtCore.QCoreApplication.instance().quit()

    def OnListClick(self):
        i = self.lwOptions.currentIndex().row()
        self.swSelection.setCurrentIndex(i)

    def OnConnectQuickClick(self):
        self.NordConnectQuick()

    def OnDisconnectQuickClick(self):
        self.NordDisconnect()

    def OnConnectListClick(self):
        c1 = ''
        if self.cbxCountry.currentIndex() > 0:
            c1 = self.cbxCountry.currentText()
        if self.cbxCity.currentIndex() == 0:
            c2 = ''
        else:
            c2 = self.cbxCity.currentText()

        self.NordConnectByCountry(c1, c2)

    def OnDisconnectListClick(self):
        self.NordDisconnect()

    def OnConnectCodeClick(self):
        self.NordCommand('nordvpn connect {}'.format(self.leCode.text()))

    def OnDisconnectCodeClick(self):
        self.NordDisconnect()

    def NordCommand(self, cmd):
        reply = os.popen(cmd).read()
        log.info(reply)
        self.pteLog.appendPlainText(reply)
        return reply

    def NordConnectQuick(self):
        self.NordCommand('nordvpn connect')

    def NordDisconnect(self):
        self.NordCommand('nordvpn disconnect')

    def NordConnectByCountry(self, Country, City):
        self.NordCommand('nordvpn connect {} {}'.format(Country, City))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
