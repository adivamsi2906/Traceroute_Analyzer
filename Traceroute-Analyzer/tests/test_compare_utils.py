import unittest
from compare_utils import compare_traceroutes
import logging

class TestCompareTraceroutes(unittest.TestCase):

    def setUp(self):
        # Set up logger to capture output
        self.logger = logging.getLogger("TracerouteLogger")
        self.logger.setLevel(logging.DEBUG)
        self.log_output = []
       
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        self.stream_handler.setFormatter(formatter)
       
        self.logger.addHandler(self.stream_handler)

        # Redirect stream output to our list
        import io
        self.log_capture_string = io.StringIO()
        self.stream_handler.stream = self.log_capture_string

    def tearDown(self):
        self.logger.removeHandler(self.stream_handler)

    def test_ip_change(self):
        old_data = {
            "hops": [
                {"hop": 1, "ip": "192.168.1.1", "rtts": [1, 2, 3]},
                {"hop": 2, "ip": "10.0.0.1", "rtts": [5, 5, 5]}
            ]
        }
        new_data = {
            "target": "8.8.8.8",
            "hops": [
                {"hop": 1, "ip": "192.168.1.1", "rtts": [1, 2, 3]},
                {"hop": 2, "ip": "10.0.0.99", "rtts": [5, 5, 5]}
            ]
        }

        compare_traceroutes(old_data, new_data)
        log_output = self.log_capture_string.getvalue()
        self.assertIn("IP changed", log_output)

    def test_missing_and_new_hops(self):
        old_data = {
            "hops": [
                {"hop": 1, "ip": "192.168.0.1", "rtts": [1, 1, 1]},
                {"hop": 2, "ip": "10.0.0.1", "rtts": [2, 2, 2]}
            ]
        }
        new_data = {
            "target": "example.com",
            "hops": [
                {"hop": 1, "ip": "192.168.0.1", "rtts": [1, 1, 1]},
                {"hop": 3, "ip": "8.8.8.8", "rtts": [10, 10, 10]}
            ]
        }

        compare_traceroutes(old_data, new_data)
        log_output = self.log_capture_string.getvalue()
        self.assertIn("❌ Hop 2: Previously existed but now missing", log_output)
        self.assertIn("🆕 Hop 3: NEW hop appeared", log_output)

if __name__ == '__main__':
    unittest.main()
