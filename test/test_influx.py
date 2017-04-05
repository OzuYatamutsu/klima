from test.setup_paths import *
from unittest import TestCase, main
from time import sleep
from influx.influx_adapter import *
from influx.datapoint_utils import *
from influx.measurement_strings import *


class TestInflux(TestCase):
    def setUp(self):
        self.db = get_client()
        self.temp_measurement_test_str = 'klima-test_temperature'
        self.humid_measurement_test_str = 'klima-test_humidity'

    def test_if_db_initialized(self):
        """
        Test whether we have a database object
        """

        self.assertIsNotNone(self.db)

    def test_can_write_data(self):
        """
        Tests if we can construct and write a datapoint to the database
        """

        influx_push_data(temp_val=10.0, humid_val=20.0, datapoint_type=DatapointType.SENSOR)

        # And clean up
        get_client().delete_series(influx_settings['database'], temp_measurement_str)
        get_client().delete_series(influx_settings['database'], humidity_measurement_str)

    def test_can_read_data(self):
        """
        Tests if we can read a previously written datapoint from the database
        """

        influx_push_data(temp_val=10.0, humid_val=20.0, datapoint_type=DatapointType.SENSOR)
        self.assertGreaterEqual(len(get_client().query("SELECT * FROM %s LIMIT 1" % temp_measurement_str)), 1)
        self.assertGreaterEqual(len(get_client().query("SELECT * FROM %s LIMIT 1" % humidity_measurement_str)), 1)

        # And clean up
        get_client().delete_series(influx_settings['database'], temp_measurement_str)
        get_client().delete_series(influx_settings['database'], humidity_measurement_str)

    def test_can_query_for_previous_timescale(self):
        """
        Tests whether we can get a previous datapoint from a previous time
        """

        influx_push_data(temp_val=10.0, humid_val=20.0, datapoint_type=DatapointType.SENSOR)

        # Wait 2 seconds before query
        sleep(2)

        self.assertGreaterEqual(len(get_data_at_relative_time(temp_measurement_str, '1s')), 1)
        self.assertGreaterEqual(len(get_data_at_relative_time(humidity_measurement_str, '1s')), 1)

if __name__ == '__main__':
    main()
