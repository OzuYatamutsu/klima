from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL
from sensors.sensor_type import SensorType

'''
Sensor data location - IMPORTANT!
Replace value below with the /dev location of your data streams.

It is expected that reading these location will return a single numerical value.

Valid values for type are SensorType.FILE (if locations point to a file) 
or SensorType.SERIAL (if they point to serial interfaces)
'''

sensors = {
    'temperature': '~/dev/test_0',
    'humidity': '~/dev/test_1',
    'type': SensorType.FILE,

    # Ignore these if type is not set to SERIAL
    'baud': 9600,
    'timeout': 1
}

# Logging
log_level = DEBUG

# InfluxDB settings
influx_settings = {
    'username': 'root',
    'password': 'root',
    'hostname': 'localhost',
    'port': 8086,
    'database': '_klima_dev', 
    'ssl': False,
    'enabled': True
}
