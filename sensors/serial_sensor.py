from sensors.sensor import Sensor
from serial import Serial
from logging import getLogger
logger = getLogger(__name__)


class SerialSensor(Sensor):
    def __init__(self, serial_location, baud_rate, timeout=1):
        """
        Create a new sensor which is fed by serial data. 
        
        :param serial_location: The location of the serial object (e.g. /dev/serial0)
        :param baud_rate: The baud rate of the serial device
        :param timeout: The time to wait for a response before giving up
        """

        self.serial_stream = Serial(serial_location, baud_rate, timeout=timeout)
        super().__init__(self.serial_stream)
