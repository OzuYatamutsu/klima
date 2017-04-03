from config import influx_settings
from influx.measurement_strings import *
from influx.datapoint_utils import *
from influxdb import InfluxDBClient
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


def influx_push_data(temp_val: float, humid_val: float, datapoint_type: DatapointType) -> bool:
    """
    Pushes new temperature and humidity datapoints to InfluxDB. Set datapoint_type to 
    SENSOR if pushing local data, LOCATION if pushing online weather data.

    :return: True if the db write was successful.
    """

    db = get_client()
    temp_str = temp_measurement_str if datapoint_type is DatapointType.SENSOR else temp_location_str
    humid_str = humidity_measurement_str if datapoint_type is DatapointType.SENSOR else humidity_location_str

    temp_datapoint = construct_influx_datapoint(temp_str, temp_val)
    humid_datapoint = construct_influx_datapoint(humid_str, humid_val)

    try:
        db.write_points(temp_datapoint + humid_datapoint)
    except Exception as e:
        logger.error("Error when writing datapoints to influx: %s", e)
        return False
    logger.debug("Wrote temp and humid datapoints to influx: (%s, %s)", temp_val, humid_val)
    return True


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
