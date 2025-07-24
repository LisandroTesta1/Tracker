from typing import Tuple

import numpy as np
import cv2 as cv

from utils import validate_expression
from exceptions import WrongTypeException
from videostreams.exceptions import (
    StreamOpeningException,
    FrameMissingException,
)


class VideoInput:
    """
    This class provides the basic operations for video input stream

    Attributes
    ----------
    video_source: str
        The video input source
    video_stream: cv.VideoCapture
        The input video stream

    Methods
    -------
    open:
        Open video stream
    close:
        Close video stream
    get_video_properties: Tuple[float, int, int]
        Return fps, frame width and frame height as a tuple
    get_frame: np.ndarray
        Return the next frame read from input stream
    """

    _GST_PIPE = (
        "v4l2src device=/dev/{} ! video/x-raw, width=1280, height=720, "
        "framerate=30/1,format=YUY2 ! nvvidconv ! video/x-raw(memory:NVMM) ! "
        "nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, "
        "format=BGR ! appsink"
    )

    def __init__(self, video_source: str):
        """
        Class constructor

        Parameters
        ----------
        video_source: str
            The input video source
        """

        validate_expression(
            isinstance(video_source, str),
            WrongTypeException(
                current_type=type(video_source).__name__,
                variable_name="source",
                expected_type="str",
            ),
        )
        self._video_source = video_source
        self._video_stream = None

    def open(self):
        """
        Open the input video stream and load the video properties.

        Raises
        ------
        StreamOpeningException
            Raised if video stream could not be opened
        """
        # Open video stream
        self._video_stream = cv.VideoCapture(0, cv.CAP_V4L)

        validate_expression(
            self._video_stream.isOpened(),
            StreamOpeningException(self._video_source),
        )

    def close(self):
        """
        Close and release the input video device
        """
        self._video_stream.release()

    def get_video_properties(self) -> tuple:
        """
        Retrieves FPS, and frame width and height.

        Returns
        -------
        tuple
            The values of fps, frame width and frame height as a tuple
        """
        # Get properties of input video stream
        video_fps = self._video_stream.get(cv.CAP_PROP_FPS)
        frame_width = self._video_stream.get(cv.CAP_PROP_FRAME_WIDTH)
        frame_height = self._video_stream.get(cv.CAP_PROP_FRAME_HEIGHT)

        return (video_fps, frame_width, frame_height)

    def get_frame(self) -> np.ndarray:
        """
        Reads the next frame from the input video source and
        returns it.

        Returns
        -------
        np.ndarray
            A frame in np.ndarray format

        Raises
        ------
        FrameMissingException
            If a new frame could not be read
        """
        # Read next frame from input stream
        ret, frame = self._video_stream.read()

        # Check if new frame was returned successfully
        if ret == False:
            raise FrameMissingException()
        else:
            return frame
