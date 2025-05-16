import unittest
import jef
from jef.nerve_agent import score

class NerveAgentTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.harmful_substances.nerve_agent")
        self.assertTrue(score_file_name == "score_v1")

if __name__ == '__main__':
    unittest.main()