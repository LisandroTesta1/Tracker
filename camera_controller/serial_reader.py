import serial
from threading import Thread
from . import visca_packet as vp
import queue
import time


class SerialReader(Thread):
    def __init__(self, serialport, queue):
        Thread.__init__(self)
        self.__port = serialport
        self.__queue = queue

    def run(self):
        """
        Read data from serial port, build VISCA packets from that stream and
        queues them.
        """
        # Run forever
        while True:
            # Check for new incoming data
            if self.__port.in_waiting:
                # Read the data
                stream = self.__port.read(vp.MAX_VISCA_PACKET_SIZE)
                # Split the read data into responses. There could be more
                # than one response in the input buffer.
                responses = stream.split(b"\xFF")
                # For each response, build a VISCA packet and queues it
                for response in responses:
                    if response != b"":
                        packet = vp.VISCAPacket(
                            response[0] - 0x80, tuple(response[1:])
                        )
                        self.__queue.put(packet)
            else:
                time.sleep(0.01)
