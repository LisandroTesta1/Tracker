import serial
from . import serial_writer as sw
from . import serial_reader as sr
from . import visca_packet as vp
import queue
from threading import Thread


class VISCAResponseAnalyzer(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.__queue = queue


    def run(self):
        while True:
            try:
                data = self.__queue.get(block=True, timeout=None)
            except queue.Empty:
                print("No data")
            else:
                print("{}{}{}".format(data.get_header(), data.get_message(),\
                    0xFF))
