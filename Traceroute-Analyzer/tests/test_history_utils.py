import unittest
import os
import json
import shutil
from datetime import datetime, timedelta
from history_utils import load_latest_traceroute

class TestHistoryUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = "results"
        os.makedirs(self.test_dir, exist_ok=True)

        self.target = "8.8.8.8"

        self.file1 = os.path.join(self.test_dir, "traceroute_8_8_8_8_20230101_120000.json")
        self.file2 = os.path.join(self.test_dir, "traceroute_8_8_8_8_20230102_120000.json")

        data1 = {
            "target": self.target,
            "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
            "hops": [{"hop": 1, "ip": "192.168.1.1", "rtts": [1, 1, 1]}]
        }

        data2 = {
            "target": self.target,
            "timestamp": datetime.now().isoformat(),
            "hops": [{"hop": 1, "ip": "192.168.1.1", "rtts": [2, 2, 2]}]
        }

        with open(self.file1, "w") as f:
            json.dump(data1, f)

        with open(self.file2, "w") as f:
            json.dump(data2, f)

        # Set custom modification times
        os.utime(self.file1, (datetime.now().timestamp() - 60, datetime.now().timestamp() - 60))
        os.utime(self.file2, (datetime.now().timestamp(), datetime.now().timestamp()))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_loads_most_recent_file(self):
        result = load_latest_traceroute(self.target)
        self.assertEqual(result["hops"][0]["rtts"], [2, 2, 2])

if __name__ == "__main__":
    unittest.main()
