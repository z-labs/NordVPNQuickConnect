import sys
import os

from nordvpn import NordVPN

import simplelogging

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget)

from UI_maindlg import Ui_Dialog

revision = '1.1'

about = """
Revision: 1.00
License: GPL-3
"""


DEBUG = False

LOG_CONSOLE_FORMAT = "%(log_color)s%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):: %(message)s%(reset)s"
LOG_FILE_FORMAT = "%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):: %(message)s"

if DEBUG:
    log = simplelogging.get_logger(file_format=LOG_FILE_FORMAT, console_format=LOG_CONSOLE_FORMAT, file_name='log.log')
else:
    log = simplelogging.get_logger(file_format=LOG_FILE_FORMAT, console_format=LOG_CONSOLE_FORMAT)

nord = NordVPN()

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

        nord.terminal = self.pteLog

        self.swSelection.setCurrentIndex(0)
        self.cbxCode.setVisible(False)
        self.resize(560, 320)

        self.LoadCountries()

        if nord.updateAvailable:
            self.lblUpdate.setText("<font color='red'>NordVPN Update Available</font>")

        self.lwOptions.clicked.connect(self.OnListClick)
        self.pbClose.clicked.connect(self.OnCloseClick)
        self.cbViewTerminal.stateChanged.connect(self.OnViewTerminalChange)
        self.lblRevision.setText(revision)

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

        # Check status
        self.pbStatusCheck.clicked.connect((self.OnStatusCheckClick))

    def LoadCountries(self):
        self.cbxCountry.clear()
        self.cbxCountry.addItem('Select Country')
        countries = nord.GetCountries().split(',')
        self.cbxCountry.addItems(countries)

    def LoadCities(self):
        self.pbConnectList.setEnabled(True)
        self.cbxCity.clear()
        self.cbxCity.addItem('Select City')
        cities = nord.GetCities(self.cbxCountry.currentText()).split(',')
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
        nord.Connect()

    def OnDisconnectQuickClick(self):
        nord.Disconnect()

    def OnConnectListClick(self):
        country = ''
        if self.cbxCountry.currentIndex() > 0:
            country = self.cbxCountry.currentText()
        if self.cbxCity.currentIndex() == 0:
            city = ''
        else:
            city = self.cbxCity.currentText()

        nord.ConnectByCountry(country, city)

    def OnDisconnectListClick(self):
        nord.Disconnect()

    def OnConnectCodeClick(self):
        nord.ConnectByServerCode(self.leCode.text())

    def OnDisconnectCodeClick(self):
        nord.Disconnect()

    def OnStatusCheckClick(self):
        self.teStatus.clear()
        self.teStatus.append(nord.GetStatus())
        self.teStatus.append(nord.GetAccount())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
