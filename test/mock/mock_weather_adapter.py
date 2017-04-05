from location.weather_adapter import WeatherAdapter

class MockWeatherAdapater(WeatherAdapter):
    """
    Grabs weather data from a remote source
    """

    def get_outside_temp(self) -> float:
        return 1.1

    def get_outside_humidity(self) -> float:
        return 50.0
