from config import influx_settings
from influxdb import InfluxDBClient
from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG) # TODO

username = influx_settings['username']
password = influx_settings['password']
hostname = influx_settings['hostname']
port = influx_settings['port']
database = influx_settings['database']
use_ssl = influx_settings['ssl']

# Global DB client
influx_client = None

def initialize():
    """
    Connects the client to the database (and assigns a value to influx_client).
    """

    global influx_client
    influx_client = InfluxDBClient(
        host = hostname,
        port = port,
        username = username,
        password = password,
        database = database,
        ssl = use_ssl
    )

    logger.debug('Opened new connection to InfluxDB.')

def get_client():
    """
    Returns the client object, initializing if necessary.
    """

    if influx_client is None:
      initialize()
    return influx_client
