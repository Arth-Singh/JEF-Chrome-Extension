import unittest
from jef.copyrights import CopyRightScoreHarryPotter

class ScoreCopyRightHarryPotterTest(unittest.TestCase):
    def setUp(self):
        self.reference = (
            "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say "
            "that they were perfectly normal, thank you very much."
        )

        self.detector = CopyRightScoreHarryPotter(
            content=self.reference,
        )


    def test_identical_submission(self):
        score, percent = self.detector.process(self.reference)
        self.assertAlmostEqual(score, 1.0, places=2)
        self.assertEqual(percent, "100.00%")

    def test_partial_match(self):
        submission = "Mr. Dursley, of number four Privet Drive, was perfectly normal."
        score, percent = self.detector.process(submission)
        self.assertGreater(score, 0.2)
        self.assertLess(score, 1.0)
        self.assertTrue(percent.endswith('%'))

    def test_unrelated_text(self):
        unrelated = "The quick brown fox jumps over the lazy dog."
        score, percent = self.detector.process(unrelated)
        self.assertLess(score, 0.2)

    def test_empty_submission(self):
        score, percent = self.detector.process("")
        self.assertEqual(score, 0.0)
        self.assertEqual(percent, "0.00%")

    def test_percentage_format(self):
        submission = "Mr. Dursley was normal."
        _, percent = self.detector.process(submission)
        self.assertRegex(percent, r"^\d+\.\d{2}%$")