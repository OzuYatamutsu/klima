from influx.influx_adapter import *
from influx.datapoint_utils import DatapointType
from location.weather_adapter import *
from time import sleep
from config import *
from sensors.sensor import Sensor
from sensors.file_sensor import FileSensor
from sensors.serial_sensor import SerialSensor
from logging import basicConfig, getLogger

# Set up logger
basicConfig(level=log_level)
logger = getLogger(__name__)

# Sensor objects
temp_sensor: Sensor = None
humid_sensor: Sensor = None

# Current readings
current_temp = 0.0
current_humidity = 0.0
current_location_temp = 0.0
current_location_humidity = 0.0

def main():
    """
    The entrypoint of the program.
    """
    global temp_sensor
    global humid_sensor

    if sensor_settings['type'] is SensorType.FILE:
        temp_sensor = FileSensor(sensor_settings['temperature'])
        humid_sensor = FileSensor(sensor_settings['humidity'])

    elif sensor_settings['type'] is SensorType.SERIAL:
        temp_sensor = SerialSensor(
            sensor_settings['temperature'],
            sensor_settings['baud'],
            sensor_settings['timeout']
        )

        humid_sensor = SerialSensor(
            sensor_settings['humidity'],
            sensor_settings['baud'],
            sensor_settings['timeout']
        )

    poll_loop()


def poll_loop():
    """Repeatedly polls for new data."""

    global current_temp
    global current_humidity
    global current_location_temp
    global current_location_humidity

    while True:
        temp_val = temp_sensor.read_data().strip()
        humid_val = humid_sensor.read_data().strip()

        if len(temp_val) > 0:
            logger.debug('Got a new temperature value! %s', temp_val)
            current_temp = float(temp_val)

        if len(humid_val) > 0:
            logger.debug('Got a new humidity value! %s', humid_val)
            current_humidity = float(humid_val)

        if location_settings['enabled']:
            logger.debug('Collecting location temp/humiditiy from remote')
            current_location_temp = get_outside_temp()
            current_location_humidity = get_outside_humidity()

            logger.debug('Got the following remote temp/humidity: (%s, %s)',
                         str(current_location_temp), str(current_location_humidity))

        if influx_settings['enabled']:
            influx_push_data(
                current_temp,
                current_humidity,
                DatapointType.SENSOR
            )

            if location_settings['enabled']:
                influx_push_data(
                    current_location_temp,
                    current_location_humidity,
                    DatapointType.LOCATION
                )

        # Wait poll_rate before reading vals again
        sleep(poll_rate)


try:
    main()
except KeyboardInterrupt:
    logger.info("KeyboardInterrupt - Closing streams and shutting down.")
    if temp_sensor is not None:
        temp_sensor.close()
    if humid_sensor is not None:
        humid_sensor.close()
