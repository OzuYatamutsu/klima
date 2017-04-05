from location.weather_adapter import WeatherAdapter
from random import randrange


class MockWeatherAdapater(WeatherAdapter):
    """
    Grabs weather data from a remote source
    """

    def get_outside_temp(self) -> float:
        return 1.1 + randrange(0, 10)

    def get_outside_humidity(self) -> float:
        return 50.0 + randrange(0, 10)
