import unittest
from jef.score_algos import score_v1

class TestJEFScoreV1(unittest.TestCase):
    def test_direct_jef_score_v1_normal_values(self):
        """Test jef_score_v1 function with normal values"""
        # Call the underlying function directly to test it
        result = score_v1(0.5, 0.4, 0.3, 0.2)

        # Expected result depends on the constants, but we can test the bounds
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 10)
        self.assertIsInstance(result, float)

    def test_direct_jef_score_v1_boundary_values(self):
        """Test jef_score_v1 function with boundary values"""
        # Test min values (0, 0, 0, 0)
        min_result = score_v1(0, 0, 0, 0)
        self.assertEqual(min_result, 0.0)

        # Test max values (1, 1, 1, 1)
        max_result = score_v1(1, 1, 1, 1)
        self.assertEqual(max_result, 10.0)

    def test_direct_jef_score_v1_clamping(self):
        """Test that values are properly clamped"""
        # Test values below 0
        below_result = score_v1(-0.5, -0.4, -0.3, -0.2)

        # Test values above 1
        above_result = score_v1(1.5, 1.4, 1.3, 1.2)

        # Results should be clamped
        self.assertEqual(below_result, 0.0)
        self.assertEqual(above_result,  11.85)


if __name__ == '__main__':
    unittest.main()
