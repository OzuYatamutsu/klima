from config import weather_settings
from logging import getLogger
logger = getLogger(__name__)


def get_outside_temp() -> float:
    """
    Returns the current outside temperature for the configured location (in Celsius).
    """
    # weather_settings['location']
    pass


def get_outside_humidity() -> float:
    """
    Returns the current outside relative humidity for the configured location.
    """
    # weather_settings['location']
    pass
