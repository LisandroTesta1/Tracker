from datetime import datetime
from typing import Tuple

import numpy as np
import cv2 as cv

from utils import validate_expression
from exceptions import WrongTypeException


class VideoOutput:
    """
    This class provides support for video stream writing.

    Attributes
    ----------
    outfile: str
        Name for output file.
    videoprops: Tuple[float]
        A tuple that contains video fps, frame width and frame height.

    Methods
    -------
    open():
        Open video stream for file writing
    close():
        Close output video stream
    write(np.ndarray):
        Write a new frame into video file
    set_video_properties(int,int):
        Set frame width and frame height for output video file
    """

    # GStreamer pipeline for video output
    _GST_PIPE = "appsrc ! autovideoconvert ! x265enc ! matroskamux ! \
        filesink location="

    _VIDEO_CODEC_FOURCC = "H265"
    _VIDEO_FPS_IDX = 0
    _VIDEO_FRAME_WIDTH_IDX = 1
    _VIDEO_FRAME_HEIGHT_IDX = 2

    def __init__(
        self,
        out_file: str,
        video_props: tuple = (30.0, 640, 480),
    ):
        """
        Class constructor

        Parameters
        ----------
        out_file: str
            Name for output file
        video_props: Tuple[float]
            Video properties as a tuple (fps, frame_width, frame_height)
        """
        validate_expression(
            isinstance(outfile, str),
            WrongTypeException(
                current_type=type(out_file).__name__,
                variable_name="out_file",
                expected_type="str",
            ),
        )

        validate_expression(
            isinstance(video_props, Tuple),
            WrongTypeException(
                current_type=type(video_props).__name__,
                variable_name="video_props",
                expected_type="tuple",
            ),
        )

        self._filename = out_file
        self._video_fps = video_props[self._VIDEO_FPS_IDX]
        self._frame_width = video_props[self._VIDEO_FRAME_WIDTH_IDX]
        self._frame_height = video_props[self._VIDEO_FRAME_HEIGHT_IDX]

        self._output_stream = None

    def open(self):
        """
        Open output video stream to write a video file
        """

        # Open video codec
        fourcc = cv.VideoWriter_fourcc(*self._VIDEO_CODEC_FOURCC)

        # Check if no name for video output file was given
        if not self._filename:
            # Get current datetime for video naming
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._filename = "output_{}.mkv".format(now)

        # Video Writers for video recording
        self._output_stream = cv.VideoWriter(
            "{}{}".format(self._GST_PIPE, self._filename),
            cv.CAP_GSTREAMER,
            fourcc,
            self._video_fps,
            (self._frame_width, self._frame_height),
            True,
        )

    def close(self):
        """
        Close output stream
        """
        self._output_stream.release()

    def write(self, frame: np.ndarray):
        """
        Write a frame into video file

        Parameters
        ----------
        frame: np.ndarray
            The frame to be written
        """
        self._output_stream.write(frame)

    @property
    def video_fps(self) -> float:
        """
        Returns video fps
        """
        return self._video_fps

    @video_fps.setter
    def video_fps(self, fps: float):
        """
        Set video fps

        Parameter
        ---------
        fps: float
            Frames per second
        """
        self._video_fps = fps

    @property
    def frame_width(self) -> int:
        """
        Returns frame width in pixels
        """
        return self._frame_width

    @frame_width.setter
    def frame_width(self, frame_width: int):
        """
        Set frame width

        Parameters
        ----------
        frame_width: int
            Frame width in pixels
        """
        self._frame_width = frame_width

    @property
    def frame_height(self) -> int:
        """
        Return frame height in pixels
        """
        return self._frame_height

    @frame_height.setter
    def frame_height(self, frame_height: int):
        """
        Set frame height

        Parameters
        ----------
        frame_height: int
            Frame height in pixels
        """
        self._frame_height = frame_height

    def set_frame_dimensions(self, frame_width: int, frame_height: int):
        """
        Set dimensions of the output frame

        Parameters
        ----------

        """
        self._frame_width = frame_width
        self._frame_height = frame_height
