import unittest
import json
import jef
from jef.tiananmen import score

class TiananmenScoreTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.chinese_censorship.tiananmen")
        self.assertTrue(score_file_name == "score_v1")

if __name__ == '__main__':
    unittest.main()
