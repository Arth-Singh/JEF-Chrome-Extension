import unittest
import jef
from jef import copyrights

class CopyrightScoreTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.copyrights")
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        sub = "This is a test sentence. Another line follows."
        ref = "This is a test sentence. Something else."
        res = copyrights.score(sub, ref)

        self.assertGreater(res["score"], 0)
        self.assertGreater(res["ngram_scores"][3], 0)
        self.assertGreater(res["sentence_scores"][0], 0)

if __name__ == '__main__':
    unittest.main()