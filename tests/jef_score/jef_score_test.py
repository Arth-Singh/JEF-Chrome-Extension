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


    def test_calculator_basic_functionality(self):
        """Test calculator with basic valid inputs."""
        result = jef.calculator(
            num_vendors=2,
            num_models=5,
            num_subjects=1,
            scores=[80.0, 90.0, 70.0]
        )

        self.assertIsInstance(result, float)

    def test_calculator_match_against_score_algo(self):
        result = jef.score(0.6, 0.4, 0.333, 0.2)
        calculator_result = jef.calculator(
            num_vendors=3,
            num_models=4,
            num_subjects=1,
            scores=[20]
        )

        self.assertEqual(result, calculator_result)

    def test_calculator_invalid_input(self):
        with self.assertRaises(AssertionError):
            jef.calculator( scores=[-1, None])

        with self.assertRaises(AssertionError):
            jef.calculator(scores=[])

        with self.assertRaises(AssertionError):
            jef.calculator(scores=[-1, 110, 200])



if __name__ == '__main__':
    unittest.main()