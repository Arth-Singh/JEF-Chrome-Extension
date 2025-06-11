import unittest
import tempfile
import os
import jef
from jef.harry_potter import score_v1 as score


class HarryPotterCopyrightScoreV1Test(unittest.TestCase):
    def setUp(self):
        f = open("assets/hpc1.txt", "r")
        self.reference = f.read()
        f.close()

    def test_identical_submission(self):
        sub = "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say "
        res = score( self.reference ,  self.reference )
        self.assertEqual(res["score"], 1.0)
        self.assertEqual(res["percentage"], 100.0)


    def test_proper_type(self):
        res = score("Mr. Dursley, of number four Privet Drive, was perfectly normal.", self.reference)
        self.assertIsInstance(res["score"], float)
        self.assertIsInstance( res["percentage"], float)


    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.copyrights.harry_potter")
        self.assertTrue(score_file_name == "score_v1")


    def test_partial_match(self):
        submission = "Mr. Dursley, of number four Privet Drive, was perfectly normal."
        res = score(submission, self.reference)
        self.assertLess(res["score"], 0.1)
        self.assertGreater(res["percentage"], 0.0)

    def test_unrelated_text(self):
        unrelated = "The quick brown fox jumps over the lazy dog."
        res = score(unrelated, self.reference)
        self.assertLess(res["score"], 0.2)


    def test_empty_submission(self):
        res = score("", self.reference)
        self.assertEqual(res["score"], 0.0)
        self.assertEqual(res["percentage"], 0.0)

if __name__ == '__main__':
    unittest.main()