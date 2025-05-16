import unittest
import jef


class TestJEFScore(unittest.TestCase):
    def test_correct_function_called(self):
        """Test that the correct version function is called"""
        score_file_name = jef.helpers.get_latest_score_version("jef.score_algos.score", r'^score_v(\d+)\.py$')
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        result = jef.score(0.5, 0.4, 0.3, 0.2)

        # Expected result depends on the constants, but we can test the bounds
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 10)
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()