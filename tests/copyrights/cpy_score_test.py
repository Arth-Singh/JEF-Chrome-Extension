import unittest
import jef
from jef.copyrights import score

class CopyrightScoreTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.copyrights")
        self.assertTrue(score_file_name == "score_v1")

if __name__ == '__main__':
    unittest.main()