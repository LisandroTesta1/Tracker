class TVTrackerException(Exception):
    """
    Base exception class
    """

    def __init__(self, msg: str):
        super(TVTrackerException, self).__init__(msg)


class WrongTypeException(TVTrackerException):
    """
    Raised when a value is not of the correct type
    """

    def __init__(
        self, current_type: str, variable_name: str, expected_type: str
    ):
        """
        Parameters
        ----------
        current_type: str
            The current type of the variable
        variable_name: str
            The name assigned to the variable
        expected_type: str
            The expected type for this variable
        """

        msg = "The type of the variable {} should be {}, but {} was \
            received".format(
            variable_name, expected_type, current_type
        )

        super().__init__(msg)