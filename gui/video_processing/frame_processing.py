from queue import Queue
from typing import Tuple
import time,serial
import threading
import cv2 as cv

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from tracking import ObjectTracker
from utils import validate_expression
from exceptions import WrongTypeException
from motores.mov_motores import ControlMotores


error_centro=(0,0)    #Error al centro, se utiliza para mover el pedestal.


class FrameProcessor(QThread):
    """
    Implements QThread interface to run the processing of frames as an
    independent thread

    Attributes
    ----------
    self._frame_size: Tuple[int]
        The size of the frame in 'x' and 'y' dimensions
    self._in_video_queue: Queue
        A queue for input video frames
    self._out_video_queue: Queue
        A queue for output video frames
    self._tracker: ObjectTracker
        A tracker instance

    Methods
    -------
    run()
        Method for thread execution
    """

    X_AXIS = 0
    Y_AXIS = 1
    MASK_BB_COLOR = (0, 0, 255)  # Mask bounding box color
    ROI_BB_COLOR = (0, 255, 0)  # ROI Bounding box color
    BB_LINE_THICKNESS = 1
    DEFECTO_AZIMUT=0
    DEFECTO_ELEVACION=0
    DEFECTO_MONTURA=serial.Serial("/dev/ttyACM0",9600)     #Se abre el puerto serial USB0	
    ROI_NUEVO_SIZE=50  #  esto se agrego 8/5/2024
    MASK_NUEVO_SIZE=26 #  esto se agrego 8/5/2024

    def __init__(
        self,
        in_video_queue: Queue,
        out_video_queue: Queue,
        estado_azimut_actual=DEFECTO_AZIMUT,
        estado_elevacion_actual=DEFECTO_ELEVACION,
        mask_nuevo_size=MASK_NUEVO_SIZE,    #  esto se agrego 8/5/2024
        roi_nuevo_size=ROI_NUEVO_SIZE,      #  esto se agrego 8/5/2024  
        montura= DEFECTO_MONTURA,
 
        
    ):
        
	#def __init__(
        #self,
        #in_video_queue: Queue,
        #out_video_queue: Queue,
        #estado_azimut_actual=DEFECTO_AZIMUT,
        #estado_elevacion_actual=DEFECTO_ELEVACION,
        #montura= DEFECTO_MONTURA,
 
        
 #   ):
 # antes era asi  8/5/2024               	

        """
        Class constructor

        Parameters
        ----------
        in_video_queue: Queue
            A queue for input video frames
        out_video_queue: Queue
            A queue for output video frames

        Raises
        ------
        WrongTypeException
            Raised if one of the parameters is not of a valid type
        """
        super(QThread, self).__init__()

        validate_expression(
            isinstance(in_video_queue, Queue),
            WrongTypeException(
                current_type=type(in_video_queue).__name__,
                variable_name="in_video_queue",
                expected_type="queue.Queue",
            ),
        )
        validate_expression(
            isinstance(out_video_queue, Queue),
            WrongTypeException(
                current_type=type(out_video_queue).__name__,
                variable_name="out_video_queue",
                expected_type="queue.Queue",
            ),
        )

        self._in_video_queue = in_video_queue
        self._out_video_queue = out_video_queue
        self._tracker = None
        self._frame_size = None
        self._current_frame = None
        self.estado_azimut_actual =estado_azimut_actual 
        self.estado_elevacion_actual =estado_elevacion_actual #24.4.24 esto estaba mal tipeado estado_azimut_actual 
        self.montura=montura
        self.roi_nuevo_size=roi_nuevo_size# esto se agrego 8/5/2024
        self.mask_nuevo_size=mask_nuevo_size # esto se agrego 8/5/2024
        
        
    def run(self):
        """
        Runs the tracking logic
        """
        while self._frame_size is None:
            pass
        
        
        self._tracker = ObjectTracker(self._frame_size,self.mask_nuevo_size,self.roi_nuevo_size)  # esto se agrego 8/5/2024
        #self._tracker = ObjectTracker(self._frame_size,26,50) 
        # 8/5/2024 era antes self._tracker = ObjectTracker(self._frame_size)
        
        while True:
            t0 = time.clock()
            self._current_frame = self._in_video_queue.get()
            print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")  
            print(self._tracker._mask_size)

            if self._tracker.is_tracking_enabled():
                self._tracker.define_roi(self._current_frame)
                status, pos = self._tracker.find_object()
                print("Tracking enable")
                if status == True:
                    self._tracker.update_mask(self._current_frame, pos)
                    error_centro = self._tracker.get_position_from_center()
                    print("Tracking status true")
                    #ControlMotores.control(self,error_centro)
                    hilo = threading.Thread(target=ControlMotores.control, 
                            args=(self,error_centro))                       #El programa del control del pedestal corre en un hilo aparte
                    hilo.start()                                            #Se activa el hilo aparte
                    
                    # Draw a rectangle for detected object
                    mask_position = self._tracker.mask_bb
                    mask_size = self._tracker.mask_size
                    cv.rectangle(
                        self._current_frame,
                        mask_position,
                        (
                            mask_position[self.X_AXIS] + mask_size,
                            mask_position[self.Y_AXIS] + mask_size,
                        ),
                        color=self.MASK_BB_COLOR,
                        thickness=self.BB_LINE_THICKNESS,
                    )

                    # Draw a rectangle for ROI
                    roi_position = self._tracker.roi_bb
                    roi_size = self._tracker.roi_size
                    cv.rectangle(
                        self._current_frame,
                        roi_position,
                        (
                            roi_position[self.X_AXIS] + roi_size,
                            roi_position[self.Y_AXIS] + roi_size,
                        ),
                        color=self.ROI_BB_COLOR,
                        thickness=self.BB_LINE_THICKNESS,
                    )
                else:
                    print("Tracking error")
                    error_centro= (0,0)                                     #Se coloca el error en cero, para que se frene en caso de que se pierda la mascara.
                    hilo = threading.Thread(target=ControlMotores.control, 
                            args=(self,error_centro))                       #El programa del control del pedestal corre en un hilo aparte
                    hilo.start()                                            #Se activa el hilo aparte
                    #ControlMotores.frenar_motores(self)            
            self._out_video_queue.put(self._current_frame)

            t1 = time.clock()
            fps = 1 / (t1 - t0)
            print("FPS: {:.2f}".format(fps))
            
            
            # self.currentFPS.emit(fps)

    @pyqtSlot(int, int)
    def set_frame_size(self, width: int, height: int):
        """
        Slot to set frame dimensions

        Parameters
        ----------
        width: int
            The width of the input frame in pixels
        height: int
            The height of the input frame in pixels
        """
        self._frame_size = (width, height)

    @pyqtSlot(tuple)
    def new_selection(self, point: Tuple[int]):
        """
        Slot for setting a new selection point.

        Paramters
        ---------
        point: Tuple[int]
            The position of the selected pixel
        """
        self._tracker.select_mask(point, self._current_frame)
        self._tracker.tracking_enabled = True

    @pyqtSlot()
    def finish_processing(self):
        """
        Slot for finishing operation.
        """
        self.exit()

      
	   
    	


