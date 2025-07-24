from exceptions import TVTrackerException


class InvalidVideoStream(TVTrackerException):
    """
    Raised when the specified input video source is invalid
    """

    def __init__(self, source):
        """
        Class constructor

        Parameters
        ----------
        source: str
            The input video source
        """
        msg = "The input video source specified: {} is invalid".format(source)

        super(InvalidVideoStream, self).__init__(msg)


class StreamOpeningException(Exception):
    """
    Raised when an error occurs when trying to open a video stream
    """

    def __init__(self, source):
        """
        Class constructor

        Parameters
        ----------
        source: str
            Source for video stream
        """
        msg = "Can not open video stream at {}".format(source)

        super(StreamOpeningException, self).__init__(msg)


class FrameMissingException(Exception):
    """
    Raised when a frame could not be read from input video stream
    """

    def __init__(self):
        msg = "Frame could not be read from input video stream"
        super(FrameMissingException, self).__init__(msg)