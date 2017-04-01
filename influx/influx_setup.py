from config import influx_settings
from influx.influx_adapter import get_client
from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG) # TODO

database = influx_settings['database']

# Open connection
db = get_client()

# Create a new database for data, if not exists
logger.info('Creating a new database (if we don\'t have one already)')
db.create_database(database)

# We're OK now
logger.info('Done! Database is ready for writing!')
