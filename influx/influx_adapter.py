from config import influx_settings
from influxdb import InfluxDBClient
from datetime import datetime
from logging import getLogger
logger = getLogger(__name__)

username = influx_settings['username']
password = influx_settings['password']
hostname = influx_settings['hostname']
port = influx_settings['port']
database = influx_settings['database']
use_ssl = influx_settings['ssl']

# Global DB client
influx_client = None


def get_client() -> InfluxDBClient:
    """
    Returns the client object, initializing if necessary.
    """

    if influx_client is None:
        __initialize()
        __setup_database()
    return influx_client


def construct_influx_datapoint(measurement: str, *args):
    """
    Given a measurement string and at least one value, returns a 
    formatted datapoint, ready to be inserted.
    """

    json_datapoint = []

    for point in args:
        json_datapoint.append(
            {
                'measurement': measurement,
                'tags': {},
                'time': str(datetime.utcnow()),
                'fields': {
                    'value': point
                }
            }
        )

    return json_datapoint

def __initialize():
    """
    Connects the client to the database (and assigns a value to influx_client).
    """

    global influx_client
    influx_client = InfluxDBClient(
        host=hostname,
        port=port,
        username=username,
        password=password,
        database=database,
        ssl=use_ssl
    )

    logger.debug('Opened new connection to InfluxDB.')


def __setup_database():
    """
    Creates a new database on the InfluxDB server.
    """

    # Open connection
    db = influx_client

    # Create a new database for data, if not exists
    logger.info('Creating a new database (if we don\'t have one already)')
    db.create_database(database)

    # We're OK now
    logger.info('Done! Database is ready for writing!')
