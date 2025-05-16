import unittest
import jef
from jef.copyrights.harry_potter import score

class HarryPotterCopyrightScoreV1Test(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.copyrights.harry_potter")
        self.assertTrue(score_file_name == "score_v1")

if __name__ == '__main__':
    unittest.main()