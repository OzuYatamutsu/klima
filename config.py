from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL
from sensors.sensor_type import SensorType

'''
Sensor data location - IMPORTANT!
Replace value below with the /dev location of your data streams.

It is expected that reading these location will return a single numerical value.

Valid values for type are SensorType.FILE (if locations point to a file) 
or SensorType.SERIAL (if they point to serial interfaces)
'''

sensor_settings = {
    'temperature': '/Users/secollin/dev/test_0',
    'humidity': '/Users/secollin/dev/test_1',
    'type': SensorType.FILE,

    # Ignore these if type is not set to SERIAL
    'baud': 9600,
    'timeout': 1
}

'''
InfluxDB settings - configure these to point to the account you want to push timeseries data to. 
(If you don't, set enabled to False.)

Otherwise, the account here must have read/write privileges to the database specified.
If it doesn't exist, it must have (admin) privileges to create one with that name.
'''
influx_settings = {
    'username': 'root',
    'password': 'root',
    'hostname': 'localhost',
    'port': 8086,
    'database': '_klima_dev', 
    'ssl': False,
    'enabled': True
}

'''
Location settings - set to True and set your location string in order to track outside 
temperatures from a weather station (for comparison against sensor data).

Example location strings:
'location': 'Sunnyvale, CA'
'location': 'Vancouver, BC'
'location': 'Shanghai, China'
'''
location_settings = {
    'enabled': True,
    'location': 'Sunnyvale, CA'
}

# Set this to determine how often we poll for new sensor data (seconds)
poll_rate = 5

# Set this to change how chatty the logs are
log_level = DEBUG
