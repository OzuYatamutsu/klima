from influx.influx_adapter import *
from influx.datapoint_utils import DatapointType
from location.weather_adapter import WeatherAdapter
from location.wunderground_adapter import WundergroundAdapter
from time import sleep
from threading import Thread, Event
from config import *
from sensors.sensor import Sensor
from sensors.file_sensor import FileSensor
from sensors.serial_sensor import SerialSensor
from logging import basicConfig, getLogger

# Test classes
from test.mock.mock_sensor import MockSensor
from test.mock.mock_weather_adapter import MockWeatherAdapater

# Set up logger
basicConfig(level=log_level)
logger = getLogger(__name__)


class MainThread(Thread):
    def __init__(self, current_vals: dict):
        """
        Initializes a new program thread, responsible for collecting and storing data.
        
        Current data will be stored in the current_vals reference passed into this constructor.
        Pass in an empty dict for current_vals.
        """

        super(MainThread, self).__init__()

        self.current_vals = current_vals
        self.stoprequest = Event()
        self.daemon = True

        # Sensor obojects
        self.temp_sensor: Sensor = None
        self.humid_sensor: Sensor = None

        # Current readings
        self.current_vals = current_vals
        self.current_vals['current_temp'] = 0.0
        self.current_vals['current_humidity'] = 0.0
        self.current_vals['current_location_temp'] = 0.0
        self.current_vals['current_location_humidity'] = 0.0

        if sensor_settings['type'] is SensorType.FILE:
            self.temp_sensor = FileSensor(sensor_settings['temperature'])
            self.humid_sensor = FileSensor(sensor_settings['humidity'])

        elif sensor_settings['type'] is SensorType.SERIAL:
            self.temp_sensor = SerialSensor(
                sensor_settings['temperature'],
                sensor_settings['baud'],
                sensor_settings['timeout']
            )

        # For Travis
        elif is_testing:
            self.temp_sensor = MockSensor()
            self.humid_sensor = MockSensor()

    def run(self):
        """
        Starts the program thread.
        """

        while not self.stoprequest.is_set():
            temp_val = self.temp_sensor.read_data().strip()
            humid_val = self.humid_sensor.read_data().strip()

            if len(temp_val) > 0:
                logger.debug('Got a new temperature value! %s', temp_val)
                self.current_vals['current_temp'] = float(temp_val)

            if len(humid_val) > 0:
                logger.debug('Got a new humidity value! %s', humid_val)
                self.current_vals['current_humidity'] = float(humid_val)

            if location_settings['enabled']:
                remote_querier: WeatherAdapter = WundergroundAdapter() if not is_testing else MockWeatherAdapater
                logger.debug('Collecting location temp/humiditiy from remote')
                self.current_vals['current_location_temp'] = remote_querier.get_outside_temp()
                self.current_vals['current_location_humidity'] = remote_querier.get_outside_humidity()

                logger.debug('Got the following remote temp/humidity: (%s, %s)',
                             str(self.current_vals['current_location_temp']),
                             str(self.current_vals['current_location_humidity'])
                             )

            if influx_settings['enabled']:
                influx_push_data(
                    self.current_vals['current_temp'],
                    self.current_vals['current_humidity'],
                    DatapointType.SENSOR
                )

                if location_settings['enabled']:
                    influx_push_data(
                        self.current_vals['current_location_temp'],
                        self.current_vals['current_location_humidity'],
                        DatapointType.LOCATION
                    )

            # Wait poll_rate before reading vals again
            sleep(poll_rate)

    def join(self, timeout=None):
        """
        Cleanly terminates the program thread.
        """

        self.stoprequest.set()

        logger.info("Received join signal - Closing streams and shutting down.")
        self.__shutdown_streams()
        super(MainThread, self).join(timeout)

    def __shutdown_streams(self):
        """
        Closes data streams for sensors.
        """
        if self.temp_sensor is not None:
            logger.debug('Closing temp sensor.')
            self.temp_sensor.close()
        if self.humid_sensor is not None:
            logger.debug('Closing humid sensor.')
            self.humid_sensor.close()
