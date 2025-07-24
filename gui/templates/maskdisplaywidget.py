# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maskdisplay.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MaskPanel(object):
    def setupUi(self, MaskPanel):
        MaskPanel.setObjectName("MaskPanel")
        MaskPanel.resize(545, 300)
        self.maskDisplay = QtWidgets.QLabel(MaskPanel)
        self.maskDisplay.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.maskDisplay.setText("")
        self.maskDisplay.setObjectName("maskDisplay")
        self.maskSizeLabel = QtWidgets.QLabel(MaskPanel)
        self.maskSizeLabel.setGeometry(QtCore.QRect(340, 10, 54, 17))
        self.maskSizeLabel.setObjectName("maskSizeLabel")
        self.fpsLabel = QtWidgets.QLabel(MaskPanel)
        self.fpsLabel.setGeometry(QtCore.QRect(340, 220, 31, 31))
        self.fpsLabel.setObjectName("fpsLabel")
        self.pointLabel = QtWidgets.QLabel(MaskPanel)
        self.pointLabel.setGeometry(QtCore.QRect(340, 260, 41, 31))
        self.pointLabel.setObjectName("pointLabel")
        self.pointValue = QtWidgets.QLabel(MaskPanel)
        self.pointValue.setGeometry(QtCore.QRect(390, 260, 150, 31))
        self.pointValue.setMinimumSize(QtCore.QSize(150, 0))
        self.pointValue.setFrameShape(QtWidgets.QFrame.Box)
        self.pointValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.pointValue.setText("")
        self.pointValue.setScaledContents(True)
        self.pointValue.setObjectName("pointValue")
        self.fpsValue = QtWidgets.QLabel(MaskPanel)
        self.fpsValue.setGeometry(QtCore.QRect(390, 220, 61, 31))
        self.fpsValue.setFrameShape(QtWidgets.QFrame.Box)
        self.fpsValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fpsValue.setText("")
        self.fpsValue.setObjectName("fpsValue")
        self.maskSizeValue = QtWidgets.QLineEdit(MaskPanel)
        self.maskSizeValue.setGeometry(QtCore.QRect(340, 30, 71, 29))
        self.maskSizeValue.setMaxLength(3)
        self.maskSizeValue.setFrame(True)
        self.maskSizeValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maskSizeValue.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.maskSizeValue.setObjectName("maskSizeValue")
        self.maskSizeSetButton = QtWidgets.QPushButton(MaskPanel)
        self.maskSizeSetButton.setGeometry(QtCore.QRect(430, 30, 41, 29))
        self.maskSizeSetButton.setObjectName("maskSizeSetButton")

        self.retranslateUi(MaskPanel)
        QtCore.QMetaObject.connectSlotsByName(MaskPanel)

    def retranslateUi(self, MaskPanel):
        _translate = QtCore.QCoreApplication.translate
        MaskPanel.setWindowTitle(_translate("MaskPanel", "Form"))
        self.maskSizeLabel.setText(_translate("MaskPanel", "Mask Size"))
        self.fpsLabel.setText(_translate("MaskPanel", "FPS"))
        self.pointLabel.setText(_translate("MaskPanel", "Point"))
        self.maskSizeValue.setInputMask(_translate("MaskPanel", "000"))
        self.maskSizeSetButton.setText(_translate("MaskPanel", "Set"))
