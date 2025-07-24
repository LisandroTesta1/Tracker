from typing import Tuple

import numpy as np
import cv2 as cv

from utils import validate_expression
from exceptions import WrongTypeException


class ObjectTracker:
    """
    This class provides all the features and operations for object tracking,
    given an image and an initial point. From this starting point, both the
    mask and ROI are defined.

    Attributes
    ----------
    frame_dims: Tuple[int]
        width and height (in pixels) of the image to be processed.
    masksize: int
        size of both width and height (in pixels) of the mask, for target
        selection. (default = 101)
    roisize: int
        size of both width and height (in pixels) of the region of interest.
        (default = 200)

    Methods
    -------

    """

    # Default values for tracking algorithm parameters
    _MATCH_THRESHOLD = 0.6
    _TEMPLATE_SIZE = 100
    _DEFAULT_MASKSIZE = _TEMPLATE_SIZE + 1
    _DEFAULT_ROISIZE = _TEMPLATE_SIZE * 2

    # For points or pixel positions
    X_AXIS = 0
    Y_AXIS = 1

    def __init__(
        self,
        frame_dims: Tuple[int],
        mask_size: int = _DEFAULT_MASKSIZE,
        roi_size: int = _DEFAULT_ROISIZE,
    ):
        """
        Class constructor

        Parameters
        ----------
        frame_dims: Tuple[int]
            The dimensions of the input frames. This value is expressed as
            (width, height)
        mask_size: int
            The size of the mask side in pixels
        roi_size: int
            The size of the ROI side in pixels

        Raises
        ------
        WrongTypeException:
            Raised if any of the parameters are not of the correct type
        """

        validate_expression(
            isinstance(frame_dims, tuple),
            WrongTypeException(
                current_type=type(frame_dims).__name__,
                variable_name="frame_dims",
                expected_type="Tuple[int, int]",
            ),
        )
        validate_expression(
            isinstance(mask_size, int),
            WrongTypeException(
                current_type=type(mask_size).__name__,
                variable_name="mask_size",
                expected_type="int",
            ),
        )
        validate_expression(
            isinstance(roi_size, int),
            WrongTypeException(
                current_type=type(roi_size).__name__,
                variable_name="roi_size",
                expected_type="int",
            ),
        )

        self._frame_dims = frame_dims
        self._mask_size = mask_size
        self._roi_size = roi_size
        self._mask_pixels = None  # Mask pixels
        self._mask_bb = None  # Upper-left mask point
        self._roi_pixels = None  # ROI pixels
        self._roi_bb = None  # Upper-left ROI point

        self._image_quadrant_limits = {
            "UPPER": self._frame_dims[self.Y_AXIS] // 2,
            "LOWER": self._frame_dims[self.Y_AXIS],
            "LEFT": self._frame_dims[self.X_AXIS] // 2,
            "RIGHT": self._frame_dims[self.X_AXIS],
        }
        self._tracking_enabled = False
        self._new_target = False

    @property
    def frame_dims(self) -> Tuple[int]:
        """
        Retrieves the dimensions of the input frame

        Returns
        -------
        Tuple[int]
            The shape of the frame as (width, height)
        """
        return self._frame_dims

    @frame_dims.setter
    def frame_dims(self, frame_dims: Tuple[int]):
        """
        Set the frame dimensions

        Parameters
        ----------
        frame_dims: Tuple[int]
            The shape of the frame as (width, height)
        """
        self._frame_dims = frame_dims


    @property
    def mask_size(self) -> int:
        """
        Retrieves the size of the mask side in pixels

        Returns
        -------
        int
            The size of the mask side in pixels
        """
        return self._mask_size

    @mask_size.setter
    def mask_size(self, mask_size: int):
        """
        Configures the mask size

        Parameters
        ----------
        mask_size: int
            The size of the mask side in pixels
        """
        self._mask_size = mask_size

    @property
    def roi_size(self) -> int:
        """
        Retrieves the size of the ROI side in pixels

        Returns
        -------
        int
            The ROI side size in pixels
        """
        return self._roi_size

    @roi_size.setter
    def roi_size(self, roi_size: int):
        """
        Configures the ROI size

        Parameters
        -----------
        roi_size: int
            The size of the ROI side in pixels
        """
        self._roi_size = roi_size

    @property
    def tracking_enabled(self) -> bool:
        """
        Indicates if tracking is enabled or not

        Returns
        -------
        bool
            True if tracking is enabled; False otherwise
        """
        return self._tracking_enabled

    @tracking_enabled.setter
    def tracking_enabled(self, value: bool):
        """
        Set enabled tracking condition

        Parameters
        ----------
        value: bool
            True if tracking is enabled; False otherwise
        """
        self._tracking_enabled = value

    def is_tracking_enabled(self) -> bool:
        """
        Indicates if tracking is enabled or not

        Returns
        -------
        bool
            True if tracking is enabled; False otherwise
        """
        return self.tracking_enabled

    @property
    def new_target(self) -> bool:
        """
        Indicates if a new target was selected or not

        Returns
        -------
        bool
            True if a new target was selected; False, otherwise
        """
        return self._new_target

    @new_target.setter
    def new_target(self, value: bool):
        """
        Set new selected target condition

        Parameters
        ----------
        bool
            True for a new selected target; False otherwise
        """
        self.newtarget = value

    def is_new_target(self) -> bool:
        """
        Indicates if a new target was selected or not

        Returns
        -------
        bool
            True if a new target was selected; False, otherwise
        """
        return self.new_target

    def select_mask(self, center: Tuple[int], frame: np.ndarray):
        """
        Get the location of the upper-left point of the mask given an
        initial point (usually an initial selection) and the pixels of
        the mask.

        Parameters
        ----------
        center: Tuple[int]
            Location (x,y) of the central point of the feature
        frame: np.ndarray
            The image from which the feature is extracted
        """
        # Find the upper-left point of the mask
        self._mask_bb = self._check_boundaries(center, self._mask_size)
        # Get mask pixels
        self._mask_pixels = frame[
            self._mask_bb[self.Y_AXIS] : self._mask_bb[self.Y_AXIS]
            + self._mask_size,
            self._mask_bb[self.X_AXIS] : self._mask_bb[self.X_AXIS]
            + self._mask_size,
            :,
        ]

    @property
    def mask_pixels(self) -> np.ndarray:
        """
        Retrieves the pixels of the mask

        Returns
        -------
        np.ndarray
            An array with the pixel values of the mask
        """
        return self._mask_pixels

    @property
    def mask_bb(self) -> Tuple[int]:
        """
        Retrieves the top-left pixel position of the mask.

        Returns
        -------
        Tuple[int]
            The position of the top-left pixel of the mask
        """
        return self._mask_bb

    @property
    def roi_pixels(self) -> np.ndarray:
        """
        Retrieves the pixels of the ROI

        Returns
        -------
        np.ndarray
            AN array with the pixel values of the ROI
        """
        return self._roi_pixels

    def define_roi(self, frame: np.ndarray):
        """
        Defined the mask, the location of the ROI is calculated
        and then the pixels are obtained.

        Parameters
        ----------
        frame: np.ndarray
            The image to be processed
        """
        # Find the central pixel of the mask
        mask_center = (
            self._mask_bb[self.X_AXIS] + self._mask_size // 2,
            self._mask_bb[self.Y_AXIS] + self._mask_size // 2,
        )
        # Computes the upper-left point of the ROI (for next iteration)
        self._roi_bb = self._check_boundaries(mask_center, self._roi_size)

        # Get pixels of the ROI (for next iteration)
        self._roi_pixels = frame[
            self._roi_bb[self.Y_AXIS] : self._roi_bb[self.Y_AXIS]
            + self._roi_size,
            self._roi_bb[self.X_AXIS] : self._roi_bb[self.X_AXIS]
            + self._roi_size,
            :,
        ]

    @property
    def roi_bb(self) -> Tuple[int]:
        """
        Retrieves the top-left pixel position of the ROI.

        Returns
        -------
        Tuple[int]
            The position of the top-left pixel of the ROI
        """
        return self._roi_bb

    def update_mask(self, frame: np.ndarray, new_detection_point: Tuple[int]):
        """
        Computes the new location of the upper-left point of the mask,
        and updates the value of its pixels.

        Parameters
        ----------
        frame: np.ndarray
            The frame processed
        new_detection_point: Tuple[int]
            Location of the upper-left point of the new match
        """
        # Find absolute position of upper-left point of new detection
        self._mask_bb = (
            self._roi_bb[self.X_AXIS] + new_detection_point[self.X_AXIS],
            self._roi_bb[self.Y_AXIS] + new_detection_point[self.Y_AXIS],
        )
        # Get pixels of the new feature matching
        new_detection_pixels = frame[
            self._mask_bb[self.Y_AXIS] : self._mask_bb[self.Y_AXIS]
            + self._mask_size,
            self._mask_bb[self.X_AXIS] : self._mask_bb[self.X_AXIS]
            + self._mask_size,
            :,
        ]
        # Update mask pixel values
        self._mask_pixels = (
            self._mask_pixels * 0.9 + new_detection_pixels * 0.1
        ).astype("uint8")

    def find_object(self) -> Tuple[bool, float]:
        """
        Computes correlation coefficients between the mask and the ROI.

        Returns
        -------
        Tuple[bool, float]
            The status (True or False) of the operation
            The location of the best match.
            NOTE: If the firs returned value is False, the best match may not
            be good enough.
        """
        # Computes correlation coefficient between the mask and the ROI
        temp_matching = cv.matchTemplate(
            self._roi_pixels, self._mask_pixels, cv.TM_CCOEFF_NORMED
        )

        # Gets the maximum and minimum values from the result and
        # their locations
        (minValue, maxValue, minLoc, maxLoc) = cv.minMaxLoc(temp_matching)
        print(minValue, maxValue, minLoc, maxLoc)

        # Apply a threshold to the maximum value for matching template
        matching_success = (
            False if (maxValue <= self._MATCH_THRESHOLD) else True
        )

        return (matching_success, maxLoc)

    def get_position_from_center(self) -> Tuple[int]:
        """
        Calculates and return the difference between the center of the
        mask and the center of the image, in X and Y axis.

        Returns
        -------
        Tuple[int]
            The difference in X and Y axis from the center of the mask and the
            center of the iamge
        """
        # Computes the center point (x,y) of the image
        # TODO: This could be computed once at the beginning
        
        img_center_x = self.frame_dims[self.X_AXIS] // 2
        img_center_y = self.frame_dims[self.Y_AXIS] // 2

        # Computes the center point (x,y) of the mask
        mask_center_x = self._mask_bb[self.X_AXIS] + self._mask_size // 2
        mask_center_y = self._mask_bb[self.Y_AXIS] + self._mask_size // 2

        # Get the difference from the center of the mask to the center
        # of the image
        img_mask_diff = (
            img_center_x - mask_center_x,
            img_center_y - mask_center_y,
        )
        print("Error: {}".format(img_mask_diff))
        return img_mask_diff

    def _check_boundaries(self, center: Tuple[int], size: int) -> Tuple[int]:
        """
        Checks if the points of the feature (mask or ROI) fall into the limits
        of the image and adjust the boundaries of the feature to it.

        Parameters
        ----------
        center: Tuple[int]
            The location (x,y) of the central point of the feature.
        size: int
            The size of the feature in pixels.

        Returns
        -------
        Tuple[int]
            The fixed position of the feature regarding the boundaries of the
            image
        """
        x_pos = center[self.X_AXIS]
        y_pos = center[self.Y_AXIS]

        # Check the limit in Y axis
        if y_pos < self._image_quadrant_limits["UPPER"]:
            upper = max(0, y_pos - size // 2)
        else:
            bottom = min(
                y_pos + size // 2, self._image_quadrant_limits["LOWER"]
            )
            upper = bottom - size

        # Check the limit in X axis
        if x_pos < self._image_quadrant_limits["LEFT"]:
            left = max(0, x_pos - size // 2)
        else:
            right = min(
                self._image_quadrant_limits["RIGHT"], x_pos + size // 2
            )
            left = right - size

        return (int(left), int(upper))
