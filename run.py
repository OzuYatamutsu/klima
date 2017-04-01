from influx.influx_adapter import *
from time import sleep
from config import *
from sensors.sensor import Sensor
from sensors.file_sensor import FileSensor
from sensors.serial_sensor import SerialSensor
from logging import basicConfig, getLogger

# Set up logger
basicConfig(level=log_level)
logger = getLogger(__name__)


def main():
    """
    The entrypoint of the program.
    """

    if influx_settings['enabled']:
        get_client()

    temp_sensor = None
    humid_sensor = None
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

    poll_loop(temp_sensor, humid_sensor)


def poll_loop(temp_sensor: Sensor, humid_sensor: Sensor):
    """Repeatedly polls for new data."""

    while True:
        temp_val = temp_sensor.read_data().strip()
        humid_val = humid_sensor.read_data().strip()

        # TODO
        if len(temp_val) > 0:
            print(temp_val)
        if len(humid_val) > 0:
            print(humid_val)

        # Wait poll_rate before reading vals again
        sleep(poll_rate)

main()
