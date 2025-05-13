import unittest
from jef.copyrights import CopyRightScoreHarryPotter

class ScoreCopyRightHarryPotterTest(unittest.TestCase):
    def setUp(self):
        self.detector = CopyRightScoreHarryPotter(filename="assets/hpp1.txt")


    def test_identical_submission(self):
        with open("assets/hpp1.txt", 'r', encoding='utf-8') as f:
            example_text = f.read()
            f.close()

        score, percent = self.detector.analyze_copyright(example_text)
        self.assertAlmostEqual(score, 1.0, places=3)
        self.assertEqual(percent, "100.00%")

    def test_partial_match(self):
        submission = "Mr. Dursley, of number four Privet Drive, was perfectly normal."
        score, percent = self.detector.analyze_copyright(submission)
        self.assertLess(score, 0.1)
        self.assertTrue(percent.endswith('%'))

    def test_unrelated_text(self):
        unrelated = "The quick brown fox jumps over the lazy dog."
        score, percent = self.detector.analyze_copyright(unrelated)
        self.assertLess(score, 0.2)

    def test_empty_submission(self):
        score, percent = self.detector.analyze_copyright("")
        self.assertEqual(score, 0.0)
        self.assertEqual(percent, "0.00%")

    def test_percentage_format(self):
        submission = "Mr. Dursley was normal."
        _, percent = self.detector.analyze_copyright(submission)
        self.assertRegex(percent, r"^\d+\.\d{2}%$")