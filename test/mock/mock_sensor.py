from sensors.sensor import Sensor
from logging import getLogger
logger = getLogger(__name__)


class MockSensor(Sensor):
    def __init__(self):
        self.is_closed = False

    def read_data(self):
        return 1.5

    def close(self):
        self.is_closed = True
