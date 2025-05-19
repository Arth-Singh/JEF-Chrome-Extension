import unittest
import tempfile
import os
import jef
from jef.copyrights import score_v1 as score

class CopyrightScoreV1Test(unittest.TestCase):

    def test_score(self):
        sub = "This is a test sentence. Another line follows."
        ref = "This is a test sentence. Something else."
        res = score(sub, ref)

        self.assertGreater(res["score"], 0)
        self.assertGreater(res["ngram_scores"][3], 0)
        self.assertGreater( res["sentence_scores"][0], 0)


    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.copyrights")
        self.assertTrue(score_file_name == "score_v1")


    def test_copyright_detection(self):
        """Test copyright detection with various levels of similarity"""
        test_cases = [
            # Exact copy
            (
                "This is a test sentence for copyright detection.",
                "This is a test sentence for copyright detection.",
                1.0
            ),
            # Completely different
            (
                "This is a test sentence.",
                "Something entirely different here.",
                0.0
            ),
            # Partial similarity
            (
                "This is a test sentence for detection.",
                "This is a test phrase for checking.",
                0.5
            ),
        ]

        for submission, reference, expected_threshold in test_cases:
            with self.subTest(submission=submission):
                _score = score(submission, reference)
                # Allow for some flexibility in the exact score
                self.assertGreaterEqual(_score["last_analysis_scores"]["final_score"], expected_threshold - 0.2)
                self.assertLessEqual(_score["last_analysis_scores"]["final_score"], expected_threshold + 0.2)

if __name__ == '__main__':
    unittest.main()