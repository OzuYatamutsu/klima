from influx.influx_adapter import *
from influx.datapoint_utils import *
from unittest import TestCase, main
from web.app import app


class TestRoutes(TestCase):
    def setUp(self):
        self.db = get_client()
        self.app = app.test_client()

        # Seed database
        influx_push_data(temp_val=20.0, humid_val=55.0, datapoint_type=DatapointType.SENSOR)
        influx_push_data(temp_val=21.5, humid_val=56.0, datapoint_type=DatapointType.LOCATION)

    def test_get_base(self):
        """
        Tests if / returns both a 200 and the status page
        """

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.content_length, 0)


if __name__ == '__main__':
    main()