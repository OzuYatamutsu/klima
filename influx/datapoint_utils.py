from enum import Enum
from datetime import datetime


class DatapointType(Enum):
    """
    The type of datapoint to send (location or local sensor data)
    """

    SENSOR = 0,
    LOCATION = 1


def construct_influx_datapoint(measurement: str, *args) -> list:
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
