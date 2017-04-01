from sensors.sensor import Sensor
from logging import getLogger
logger = getLogger(__name__)


class FileSensor(Sensor):
    def __init__(self, file_location):
        """
        Create a new sensor which is fed by an updated file on the filesystem. 

        :param file_location: The location of the file
        """

        self.file_stream = open(file_location, 'r')
        super().__init__(self.file_stream)
