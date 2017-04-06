from sensors.sensor import Sensor
from random import randrange
from logging import getLogger
logger = getLogger(__name__)


class MockSensor(Sensor):
    def __init__(self):
        self.is_closed = False

    def read_data(self):
        return str(1.5 + randrange(0, 10))

    def close(self):
        self.is_closed = True
