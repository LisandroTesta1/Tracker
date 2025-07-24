# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videodisplay.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoDisplay(object):
    def setupUi(self, VideoDisplay):
        VideoDisplay.setObjectName("VideoDisplay")
        VideoDisplay.resize(1280, 720)
        self.frameDisplay = QtWidgets.QLabel(VideoDisplay)
        self.frameDisplay.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.frameDisplay.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.frameDisplay.setText("")
        self.frameDisplay.setObjectName("frameDisplay")

        self.retranslateUi(VideoDisplay)
        QtCore.QMetaObject.connectSlotsByName(VideoDisplay)

    def retranslateUi(self, VideoDisplay):
        _translate = QtCore.QCoreApplication.translate
        VideoDisplay.setWindowTitle(_translate("VideoDisplay", "Form"))
