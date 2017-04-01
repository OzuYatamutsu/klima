from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL

# Sensor data location - IMPORTANT!
# Replace value below with the /dev location of your serial devices.
# It is expected that reading these sensors will return a single numerical value:
sensors = {
    'temperature': '~/dev/test_0',
    'humidity': '~/dev/test_1'
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

