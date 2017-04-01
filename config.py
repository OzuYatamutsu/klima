from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL

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
