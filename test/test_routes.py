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

    def test_get_current_temp_or_humidity(self):
        """
        Tests if /api/<string:sensor_type> returns both a 200 and some values
        """

        response = self.app.get('/api/temperature')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'0.0')

        response = self.app.get('/api/humidity')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'0.0')

    def test_get_temp_or_humidity_at_time(self):
        """
        Tests if /api/<string:sensor_type>/<string:timescale> returns both a 200 and some values
        """

        response = self.app.get('/api/temperature/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

        response = self.app.get('/api/humidity/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

    def test_get_location_temp_or_humidity(self):
        """
        Tests if /api/<string:sensor_type>/location returns both a 200 and some values
        """

        response = self.app.get('/api/temperature/location')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'0.0')

        response = self.app.get('/api/humidity/location')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'0.0')

    def test_get_location_temp_or_humidity_at_time(self):
        """
        Tests if /api/<string:sensor_type>/location/<string:timescale> returns both a 200 and some values
        """

        response = self.app.get('/api/temperature/location/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

        response = self.app.get('/api/humidity/location/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

    def test_get_location_temp_or_humidity_diff(self):
        """
        Tests if /api/<string:sensor_type>/location/diff returns both a 200 and some values
        """

        response = self.app.get('/api/temperature/location/diff')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'0.0')

        response = self.app.get('/api/humidity/location/diff')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'0.0')

    def test_get_location_temp_or_humidity_diff_at_time(self):
        """
        Tests if /api/<string:sensor_type>/location/diff/<string:timescale> returns both a 200 and some values
        """

        response = self.app.get('/api/temperature/location/diff/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

        response = self.app.get('/api/humidity/location/diff/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

    def test_get_location_temp_or_humidity_diff_avg_at_time(self):
        """
        Tests if /api/<string:sensor_type>/location/diff/avg/<string:timescale> returns both a 200 and some values
        """

        response = self.app.get('/api/temperature/location/diff/avg/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')

        response = self.app.get('/api/humidity/location/diff/avg/5m')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'{}')


if __name__ == '__main__':
    main()
