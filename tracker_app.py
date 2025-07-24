from os import listdir

from serial.tools import list_ports

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from gui.templates.mainwindow import Ui_MainWindow
from gui.cameracontrolpanel import CameraControlPanel
from gui.videoinputwindow import VideoInputWindow


class TrackerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(TrackerApp, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """
        Initializes main window interface
        """
        # Initialize combobox lists
        self.loadSerialPortsComboBox()
        self.loadVideoSourcesComboBox()
        # Create widgets for camera control and video input
        self.camControlPanel = CameraControlPanel()
        self.videoWindow = VideoInputWindow(None,self.camControlPanel)  #8/5/2024
        # Connect widget signals/slots
        self.startVideoButton.clicked.connect(self.initVideoStream)
        self.camSerialPortButton.clicked.connect(self.initCameraControl)
        self.refreshSerialPortsButton.clicked.connect(
            self.loadSerialPortsComboBox
        )
        self.refreshVideoSourcesButton.clicked.connect(
            self.loadVideoSourcesComboBox
        )
        # Diplay window
        self.show()

    def loadSerialPortsComboBox(self):
        """
        Initializes Serial Port Combobox list
        """
        portcount = self.camSerialPortComboBox.count()
        # Delete all combo box entries
        for _ in range(portcount):
            self.camSerialPortComboBox.removeItem(0)
        # List serial ports
        serialports = [port.device for port in sorted(list_ports.comports())]
        # Set combo box list for serial ports
        self.camSerialPortComboBox.addItems(serialports)
        self.camSerialPortComboBox.setCurrentIndex(0)

    def loadVideoSourcesComboBox(self):
        """
        Initializes Serial Port Combobox list
        """
        # Delete all combo box entries
        videosourcescount = self.inputVideoComboBox.count()
        for _ in range(videosourcescount):
            self.inputVideoComboBox.removeItem(0)
        # Look for video sources in '/dev' directory
        videosources = [
            source
            for source in sorted(listdir("/dev/"))
            if source.startswith("video")
        ]
        # Set combo box entries
        self.inputVideoComboBox.addItems(videosources)
        self.inputVideoComboBox.setCurrentIndex(0)

    # Slot for Camera Control Connection
    def initCameraControl(self):
        """
        Initializes Camera Control Panel and updates Main Window
        """
        # Disables button for camera serial port connection
        self.camSerialPortButton.setEnabled(False)
        # Connect signal/slot to restore button by closing camera control panel
        self.camControlPanel.closedWindow.connect(self.restoreSerialPortButton)
        self.camControlPanel.setSerialPort(
            self.camSerialPortComboBox.currentText()
        )
        # Connect signal to control zoom from video display window
        self.videoWindow.zoom_control_signal.connect(
            self.camControlPanel.setCamZoomSliderValue
        )
        self.camControlPanel.initUi()
        self.camControlPanel.show()

    # Slot for Video Display Window
    def initVideoStream(self):
        """
        Initializes Video Display Window and updates Main Window
        """
        # Disables 'Capture' button
        self.startVideoButton.setEnabled(False)
        # Get the selected entry from combobox and set the video source
        self.videoWindow.setVideoSource(self.inputVideoComboBox.currentText())
        # Connect signal/slot to restore button by closing video display window
        self.videoWindow.closed_window_signal.connect(
            self.restoreStartVideoButton
        )
        # Initializes Video Display window
        self.videoWindow.initUi()
        self.videoWindow.show()

    # Slot for closedWindow Signal from Video Input window
    def restoreStartVideoButton(self):
        # Enables 'Start Video Capture' button
        self.startVideoButton.setEnabled(True)

    # Slot for closedWindow Signal from Camera Control panel
    def restoreSerialPortButton(self):
        self.camSerialPortButton.setEnabled(True)
