import serial
from threading import Thread
from . import visca_packet as vp
import queue


class SerialWriter(Thread):

    def __init__(self, serialport, queue):
        Thread.__init__(self)
        self.__port = serialport
        self.__queue = queue


    def run(self):
        """
        Get a pakcet from the queue and send it through the serial port
        """
        while True:
            packet = self.__queue.get(block=True)
            print(packet.get_packet_bytes())
            self.__port.write(packet.get_packet_bytes())
