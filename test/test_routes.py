from unittest import TestCase, main
from web.app import app


class TestRoutes(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_base(self):
        """
        Tests if / returns both a 200 and the status page
        """

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.content_length, 0)

if __name__ == '__main__':
    main()
