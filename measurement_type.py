from enum import Enum


class MeasurementType(Enum):
    """
    The type of measurement measured. 
    
    TEMPERATURE is temperature, in degrees Celsius,
    HUMIDITY is relative humidity (percentage)
    """
    SENSOR_TEMPERATURE = 0,
    SENSOR_HUMIDITY = 1,
    LOCATION_TEMPERATURE = 2,
    LOCATION_HUMIDITY = 3
