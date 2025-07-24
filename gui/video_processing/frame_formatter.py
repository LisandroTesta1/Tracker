from queue import Queue

import cv2 as cv

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from utils import validate_expression
from exceptions import WrongTypeException


class FrameFormatter(QThread):
    """
    Implements QThread interafce to run the frame conversions as an
    independent thread.
    This class is intended to convert images from OpenCV format to the format
    accepted by PyQt.
    """

    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, input_queue: Queue):
        """
        Class constructor

        Parameters
        ----------
        input_queue: queue.Queue
            Video input queue

        Raises
        ------
        WrongTypeException
            If the input parameters are not of the required type
        """
        super(FrameFormatter, self).__init__()

        validate_expression(
            isinstance(input_queue, Queue),
            WrongTypeException(
                current_type=type(input_queue).__name__,
                variable_name="input_queue",
                expected_type="queue.Queue",
            ),
        )
        self._input_frames = input_queue

    def run(self):
        """
        Runs the format conversion logic
        """
        while True:
            frame = self._input_frames.get()

            rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            height, weight, channels = rgb_image.shape
            # bytesPerLine = ch * w
            # convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine,
            # QImage.Format_RGB888)
            # print(rgbImage)
            convert_to_qt_format = QImage(
                rgb_image.data, weight, height, QImage.Format_RGB888
            )
            self.change_pixmap_signal.emit(convert_to_qt_format)

    @pyqtSlot()
    def finish_frame_formatting(self):
        """
        Slot for finishing opearation
        """
        self.exit()
