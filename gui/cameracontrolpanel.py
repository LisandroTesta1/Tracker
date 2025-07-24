from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from gui.templates.cameracontrolwidget import Ui_CameraControlWidget
from camera_controller.serial_reader import SerialReader
from camera_controller.serial_writer import SerialWriter
from camera_controller.visca_command_interpreter import VISCACommandInterpreter
from camera_controller.visca_response_analyzer import VISCAResponseAnalyzer
import queue
import serial

DEVICE_ADDRESS = 1

class CameraControlPanel(QtWidgets.QWidget, Ui_CameraControlWidget):

    closedWindow = pyqtSignal()

    def __init__(self, serialportname=None, parent=None):
        super(CameraControlPanel, self).__init__(parent)
        self.setupUi(self)
        self.serialportname = serialportname

    def initUi(self):
   
        try:
            self.serialport = serial.Serial(self.serialportname, baudrate=9600, timeout=0.01)
        except serial.serialutil.SerialException:
            return "Port couldn't be opened"
        else:
            # Connect to signal for slider value changes
            self.camZoomSlider.valueChanged.connect(self.setCamZoom)
            self.roiSlider.valueChanged.connect(self.setRoiSilder)# 8/5/2024
            # Create objects for camera controller
            self.cmdQueue = queue.Queue(128)
            self.responseQueue = queue.Queue(128)
            self.writer = SerialWriter(self.serialport, self.cmdQueue)
            self.reader = SerialReader(self.serialport, self.responseQueue)
            self.analyzer = VISCAResponseAnalyzer(self.responseQueue)
            self.cmdInterpreter = VISCACommandInterpreter(DEVICE_ADDRESS, self.cmdQueue)
            self.writer.start()
            self.reader.start()
            self.analyzer.start()
            self.cameraInit()


    def closeEvent(self, event):
        # TODO: Delete objects and finish all threads
        #self.disableWidgets()
        self.closedWindow.emit()
        event.accept()


    def disableWidgets(self):
        self.camZoomSlider.setEnabled(False)
        self.camFocusSlider.setEnabled(False)


    def setSerialPort(self, serialportname):
        self.serialportname = serialportname


    def cameraInit(self):
        self.cmdInterpreter.IF_Clear()
        self.cmdInterpreter.AddressSet()
#----------------------------------------------------------
    def setRoiSilder(self): #8/5/2024
        value_roi = self.roiSlider.value()
        self.roiLabelValor.setText(str(value_roi))
   
    def getRoiSilder(self): #8/5/2024
        return self.roiSlider.value()
        
#----------------------------------------------------------
    def setCamZoom(self):
        value = self.camZoomSlider.value()
        self.cmdInterpreter.CAM_Zoom('Direct', value)
        #03-05-24 agregado para poder ver el valor del zoom
        self.zoomLabelValor.setText(str(value))


    @pyqtSlot(int)
    def setCamZoomSliderValue(self, delta):
        currentValue = self.camZoomSlider.value()
        self.camZoomSlider.setValue(currentValue + delta)

