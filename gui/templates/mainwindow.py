# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(920, 524)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cameraControGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.cameraControGroupBox.setGeometry(QtCore.QRect(10, 10, 271, 181))
        self.cameraControGroupBox.setFlat(True)
        self.cameraControGroupBox.setObjectName("cameraControGroupBox")
        self.camSerialPortButton = QtWidgets.QPushButton(self.cameraControGroupBox)
        self.camSerialPortButton.setGeometry(QtCore.QRect(140, 100, 111, 51))
        self.camSerialPortButton.setObjectName("camSerialPortButton")
        self.camSerialPortLabel = QtWidgets.QLabel(self.cameraControGroupBox)
        self.camSerialPortLabel.setGeometry(QtCore.QRect(20, 30, 121, 17))
        self.camSerialPortLabel.setObjectName("camSerialPortLabel")
        self.camSerialPortComboBox = QtWidgets.QComboBox(self.cameraControGroupBox)
        self.camSerialPortComboBox.setGeometry(QtCore.QRect(20, 50, 230, 25))
        self.camSerialPortComboBox.setDuplicatesEnabled(True)
        self.camSerialPortComboBox.setObjectName("camSerialPortComboBox")
        self.refreshSerialPortsButton = QtWidgets.QPushButton(self.cameraControGroupBox)
        self.refreshSerialPortsButton.setGeometry(QtCore.QRect(20, 100, 111, 51))
        self.refreshSerialPortsButton.setObjectName("refreshSerialPortsButton")
        self.inputVideoGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.inputVideoGroupBox.setGeometry(QtCore.QRect(10, 220, 271, 181))
        self.inputVideoGroupBox.setObjectName("inputVideoGroupBox")
        self.startVideoButton = QtWidgets.QPushButton(self.inputVideoGroupBox)
        self.startVideoButton.setGeometry(QtCore.QRect(140, 100, 111, 51))
        self.startVideoButton.setObjectName("startVideoButton")
        self.inputVideoLabel = QtWidgets.QLabel(self.inputVideoGroupBox)
        self.inputVideoLabel.setGeometry(QtCore.QRect(20, 30, 121, 17))
        self.inputVideoLabel.setObjectName("inputVideoLabel")
        self.inputVideoComboBox = QtWidgets.QComboBox(self.inputVideoGroupBox)
        self.inputVideoComboBox.setGeometry(QtCore.QRect(20, 50, 230, 25))
        self.inputVideoComboBox.setObjectName("inputVideoComboBox")
        self.refreshVideoSourcesButton = QtWidgets.QPushButton(self.inputVideoGroupBox)
        self.refreshVideoSourcesButton.setGeometry(QtCore.QRect(20, 100, 111, 51))
        self.refreshVideoSourcesButton.setObjectName("refreshVideoSourcesButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cameraControGroupBox.setTitle(_translate("MainWindow", "Camera Control Connection"))
        self.camSerialPortButton.setText(_translate("MainWindow", "Connect"))
        self.camSerialPortLabel.setText(_translate("MainWindow", "Serial Port"))
        self.refreshSerialPortsButton.setText(_translate("MainWindow", "Refresh"))
        self.inputVideoGroupBox.setTitle(_translate("MainWindow", "Video Source"))
        self.startVideoButton.setText(_translate("MainWindow", "Capture"))
        self.inputVideoLabel.setText(_translate("MainWindow", "Input Video Source"))
        self.refreshVideoSourcesButton.setText(_translate("MainWindow", "Refresh"))
