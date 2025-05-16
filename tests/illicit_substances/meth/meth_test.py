import unittest
import jef
from jef.meth import score


class MethTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.illicit_substances.meth")
        self.assertTrue(score_file_name == "score_v1")


if __name__ == '__main__':
    unittest.main()