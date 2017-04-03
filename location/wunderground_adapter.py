from location.weather_adapter import WeatherAdapter
from config import location_settings
from requests import get
from re import match
from logging import getLogger
logger = getLogger(__name__)

api_location = "http://api.wunderground.com/api/%s/conditions/q/%s.json"
humidity_match = '(\d+)%?'

api_key = location_settings['api_key']
location = location_settings['location']


class WundergroundAdapter(WeatherAdapter):
    """
    Grabs weather data from a remote source
    """

    def get_outside_temp(self) -> float:
        """
        Returns the current outside temperature for the configured location (in Celsius).
        """

        result = get(api_location % (api_key, location)).json()["current_observation"]["temp_c"]
        logger.debug('Wunderground reports temp for location %s as %s', location, result)

        return result

    def get_outside_humidity(self) -> float:
        """
        Returns the current outside relative humidity for the configured location.
        """

        result = get(api_location % (api_key, location)).json()["current_observation"]["relative_humidity"]
        result = self.__wu_humidity_str_to_float(result)
        logger.debug('Wunderground reports humidity for location %s as %s', location, result)

        return result

    @staticmethod
    def __wu_humidity_str_to_float(humidity_str) -> float:
        """
        Extracts the numerical portion of a wunderground humidity string via regex
        """

        return float(
            match(humidity_match, humidity_str).group(1)
        )
