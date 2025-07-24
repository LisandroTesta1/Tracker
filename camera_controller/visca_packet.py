MAX_VISCA_PACKET_SIZE = 16

class VISCAPacket:

    def __init__(self, periph_address, message):
        """
        Initializes a packet according to VISCA specifications:

        +------------+---------------------------+------------+
        |   HEADER   |          MESSAGE          | TERMINATOR |
        |  (1 byte)  |       (1-14 bytes)        |  (1 byte)  |
        +------------+---------------------------+------------+

        Keyword argument:
        periph_address -- Address of the peripheral device (default 0)
        message -- Payload of the packet to be sent (default ''). It
            must be expressed as a tuple, e.g, 0x80AE56 must be passed
            as [0x80, 0xAE, 0x56]

        Raises:
        ValueError -- If peripheral address or message are not in its bounds
        TypeError -- If message is not a tuple of integers
        """
        # Check if message is a tuple
        if (not isinstance(message, tuple)):
            raise TypeError("Message should be a tuple of integers")
        # Check the length of the parameter 'message'
        if (len(message)<1 or len(message)>14):
            raise ValueError("Message length should be in range [1-14]")
        # Check the type of the elements in 'message'
        if not (all(isinstance(n, int) for n in message)):
            raise TypeError("Message elements must be integers")
        # Check the value of each element in 'message'
        if not (all(n in range(256) for n in message)):
            raise ValueError("Message elements must be in range [0-255]")

        self.__header = (0x80 + periph_address,)
        self.__message = message
        self.__terminator = (0xFF,)


    def set_periph_address(self, periph_address):
        # Check for peripheral address. It must be in the range [0-7]
        if (periph_address < 0x0 or periph_address > 0x7):
            raise ValueError("Peripheral address must be in [0-7]")
        else:
            self.__header = (0x80 | periph_address,)


    def set_message(self, message):
        # Check if message is a tuple
        if (not isinstance(message, tuple)):
            raise TypeError("Message should be a list of integers")
        # Check the length of the parameter 'message'
        if (len(message)<1 or len(message)>14):
            raise ValueError("Message length should be in range [1-14]")
        # Check the type of the elements in 'message'
        if not (all(isinstance(n, int) for n in message)):
            raise TypeError("Message elements must be integers")
        # Check the value of each element in 'message'
        if (all(n in range(256) for n in message)):
            raise ValueError("Message elements must be in range [0-255]")
        else:
            self.__message = message


    def get_header(self):
        return self.__header


    def get_message(self):
        return self.__message


    def get_packet_bytes(self):
        """
        Converts all fields of the package into an array of bytes

        Returns:
        A bytearray-form of the VISCA packet
        """
        packet = self.__header + self.__message + self.__terminator

        return bytearray(packet)
