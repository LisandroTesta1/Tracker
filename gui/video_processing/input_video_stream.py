from queue import Queue

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from videostreams import VideoInput
from videostreams.exceptions import FrameMissingException


class InputVideoStream(QThread):
    """
    Implements QThread interface to run the video capture logic as an
    independent thread

    Attributes
    ----------
    video_source: str
        The name of the input video source
    output_frames: queue.Queue
        The queue that stores the captured frames

    Methods
    -------
    run()
        Runs the video capture logic
    """

    # Signal for frame dimensions
    frame_dimensions_signal = pyqtSignal(int, int)

    def __init__(self, video_source: str, output_frames: Queue):
        """
        Class constructor

        Parameters
        ----------
        video_source: str
            The name of the input video source
        output_frames: queue.Queue
            A queue used to store the captured frames
        """
        super(InputVideoStream, self).__init__()
        self._video_stream = VideoInput(video_source)
        self._output_frames = output_frames

    def run(self):
        """
        Run the video capture logic
        """
        # Open video capture
        self._video_stream.open()

        # Get intput video properties
        self._get_input_video_properties()

        # Get frame from input and enqueues it
        while True:
            try:
                frame = self._video_stream.get_frame()
            except FrameMissingException:
                break
            else:
                self._output_frames.put(frame)

        # Close video input stream
        self._video_stream.close()

    def _get_input_video_properties(self):
        """
        Emit a signal with the fps and frame width and height of the
        input video stream
        """
        fps, width, height = self._video_stream.get_video_properties()
        print("FPS: {}\tResolution=({},{})".format(fps, width, height))
        # Send signal with frame dimensions
        self.frame_dimensions_signal.emit(width, height)

    @pyqtSlot()
    def finish_input_video_stream(self):
        """
        Slot to be connected for close input video stream signals
        """
        self._video_stream.close()
        self.exit()
