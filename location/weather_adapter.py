class WeatherAdapter:
    """
    Grabs weather data from a remote source
    """

    def get_outside_temp(self) -> float:
        """
        Returns the current outside temperature for the configured location (in Celsius).
        """

        raise NotImplementedError("Class was not implemented!")

    def get_outside_humidity(self) -> float:
        """
        Returns the current outside relative humidity for the configured location.
        """

        raise NotImplementedError("Class was not implemented!")
