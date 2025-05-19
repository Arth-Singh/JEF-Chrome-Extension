import unittest
import jef
from jef import harry_potter

class HarryPotterCopyrightScoreV1Test(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.copyrights.harry_potter")
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        result = harry_potter.score("Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say ", "Mr. and Mrs. Dursley, of number four Privet Drive, were proud to say ")
        self.assertEqual(result["score"], 1.0)
        self.assertEqual(result["percentage"], 100.0)

if __name__ == '__main__':
    unittest.main()