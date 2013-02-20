import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from mock import MagicMock
from konfig import Konfig
import app as flask_app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        test_config = {'sendgrid_user': 'testing',
                       'sendgrid_password': 'testing_password',
                       'email_sender': 'sender@example.com',
                       'email_send_to': 'receiver@example.com',
                       'email_send_to_name': 'Example User'}
        self.tearDown()
        self.app = flask_app.app.test_client()
        flask_app.konf = Konfig()
        flask_app.konf.use_dict(test_config)

    def test_has_default_route(self):
        path = "/"
        rv = self.app.get(path)
        self.assertEquals("200 OK", rv.status)
        self.assertEquals("Hello.", rv.data)
