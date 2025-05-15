import unittest
from jef.copyrights import CopyRightScoreHarryPotter

class ScoreCopyRightHarryPotterTest(unittest.TestCase):
    def setUp(self):
        self.detector = CopyRightScoreHarryPotter(filename="assets/hpp1.txt")


    def test_identical_submission(self):
        example_text =  "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say "
        detector = CopyRightScoreHarryPotter(content=example_text)

        res = detector.analyze(example_text)
        score = res["score"]
        percent = res["percentage"]

        self.assertAlmostEqual(score, 1.0, places=3)
        self.assertEqual(percent, 100.0)

    def test_proper_type(self):
        res = self.detector.analyze("Mr. Dursley, of number four Privet Drive, was perfectly normal.")
        score = res["score"]
        percent = res["percentage"]

        self.assertIsInstance(score, float)
        self.assertIsInstance(percent, float)


    def test_partial_match(self):
        submission = "Mr. Dursley, of number four Privet Drive, was perfectly normal."
        res = self.detector.analyze(submission)
        score = res["score"]

        self.assertLess(score, 0.1)

    def test_unrelated_text(self):
        unrelated = "The quick brown fox jumps over the lazy dog."
        res  = self.detector.analyze(unrelated)
        score = res["score"]

        self.assertLess(score, 0.2)

    def test_empty_submission(self):
        res = self.detector.analyze("")
        score = res["score"]
        percent = res["percentage"]

        self.assertEqual(score, 0.0)
        self.assertEqual(percent, 0.0)
