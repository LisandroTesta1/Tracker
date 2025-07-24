# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cameracontrolpanel.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CameraControlWidget(object):
    def setupUi(self, CameraControlWidget):
        CameraControlWidget.setObjectName("CameraControlWidget")
        CameraControlWidget.resize(202, 344)
        self.camOnOffButton = QtWidgets.QPushButton(CameraControlWidget)
        self.camOnOffButton.setEnabled(True)
        self.camOnOffButton.setGeometry(QtCore.QRect(20, 290, 161, 29))
        self.camOnOffButton.setObjectName("camOnOffButton")
        self.camZoomSlider = QtWidgets.QSlider(CameraControlWidget)
        self.camZoomSlider.setEnabled(True)
        self.camZoomSlider.setGeometry(QtCore.QRect(40, 30, 17, 160))
        self.camZoomSlider.setMaximum(16384)
        self.camZoomSlider.setOrientation(QtCore.Qt.Vertical)
        self.camZoomSlider.setObjectName("camZoomSlider")
        self.zoomLabel = QtWidgets.QLabel(CameraControlWidget)
        self.zoomLabel.setGeometry(QtCore.QRect(20, 200, 54, 17))
        self.zoomLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.zoomLabel.setObjectName("zoomLabel")

	#03-05-24 agregado para poder ver el valor del zoom
        self.zoomLabelValor = QtWidgets.QLabel(CameraControlWidget)
        self.zoomLabelValor.setGeometry(QtCore.QRect(20, 240, 91, 17))
        self.zoomLabelValor.setAlignment(QtCore.Qt.AlignCenter)
        self.zoomLabelValor.setObjectName("zoomLabelValor")
        self.zoomLabelValor.setText(str(self.camZoomSlider.value()))


        self.camFocusSlider = QtWidgets.QSlider(CameraControlWidget)
        self.camFocusSlider.setEnabled(True)
        self.camFocusSlider.setGeometry(QtCore.QRect(130, 30, 17, 160))
        self.camFocusSlider.setOrientation(QtCore.Qt.Vertical)
        self.camFocusSlider.setObjectName("camFocusSlider")
        self.camFocusLabel = QtWidgets.QLabel(CameraControlWidget)
        self.camFocusLabel.setGeometry(QtCore.QRect(120, 200, 41, 17))
        self.camFocusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.camFocusLabel.setObjectName("camFocusLabel")


        # esto se agrego 8/5/2024
        self.roiSlider = QtWidgets.QSlider(CameraControlWidget)
        self.roiSlider.setEnabled(True)
        self.roiSlider.setGeometry(QtCore.QRect(60, 260, 81, 20))
        self.roiSlider.setMaximum(200)
        self.roiSlider.setMinimum(20)
        self.roiSlider.setOrientation(QtCore.Qt.Horizontal)
        self.roiSlider.setObjectName("roiSlider")
        self.roiSlider.setValue(100)

        self.roiLabel = QtWidgets.QLabel(CameraControlWidget)
        self.roiLabel.setGeometry(QtCore.QRect(10, 260, 41, 17))
        self.roiLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.roiLabel.setObjectName("roiLabel")
       
        self.roiLabelValor = QtWidgets.QLabel(CameraControlWidget)
        self.roiLabelValor.setGeometry(QtCore.QRect(140, 260, 54, 17))
        self.roiLabelValor.setAlignment(QtCore.Qt.AlignCenter)
        self.roiLabelValor.setObjectName("roiLabelValor")
        self.roiLabelValor.setText(str(self.roiSlider.value()))
        #-----------------------------


        self.retranslateUi(CameraControlWidget)
        QtCore.QMetaObject.connectSlotsByName(CameraControlWidget)

    def retranslateUi(self, CameraControlWidget):
        _translate = QtCore.QCoreApplication.translate
        CameraControlWidget.setWindowTitle(_translate("CameraControlWidget", "Form"))
        self.camOnOffButton.setText(_translate("CameraControlWidget", "On/Off"))
        self.zoomLabel.setText(_translate("CameraControlWidget", "Zoom"))
        self.camFocusLabel.setText(_translate("CameraControlWidget", "Focus"))
        self.roiLabel.setText(_translate("CameraControlWidget", "ROI"))
