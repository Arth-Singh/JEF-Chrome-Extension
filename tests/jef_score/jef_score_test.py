import unittest
from jef.score_algos.jef_score import JEFScore

class TestJEFScore(unittest.TestCase):
    def setUp(self):
        """Set up test cases with default JEFScore instance"""
        self.jef_score = JEFScore()

    def test_initialization_default_values(self):
        """Test initialization with default values"""
        self.assertEqual(self.jef_score.bv, 0.0)
        self.assertEqual(self.jef_score.bm, 0.0)
        self.assertEqual(self.jef_score.rt, 0.0)
        self.assertEqual(self.jef_score.fd, 0.0)
        self.assertEqual(self.jef_score.opts, {})

    def test_initialization_with_values(self):
        """Test initialization with specific values"""
        score = JEFScore(bv=0.5, bm=0.6, rt=0.7, fd=0.8, opts={"test": True})
        self.assertEqual(score.bv, 0.5)
        self.assertEqual(score.bm, 0.6)
        self.assertEqual(score.rt, 0.7)
        self.assertEqual(score.fd, 0.8)
        self.assertEqual(score.opts, {"test": True})

    def test_clamp_score(self):
        """Test score clamping functionality"""
        self.assertEqual(self.jef_score.clamp_score(-0.5), 0.0)
        self.assertEqual(self.jef_score.clamp_score(0.0), 0.0)
        self.assertEqual(self.jef_score.clamp_score(0.5), 0.5)
        self.assertEqual(self.jef_score.clamp_score(1.0), 1.0)
        self.assertEqual(self.jef_score.clamp_score(1.5), 1.0)

    def test_analyze_score_zero_values(self):
        """Test JEF score calculation with zero values"""
        score = self.jef_score.analyze()
        self.assertEqual(score, 0.0)

    def test_analyze_jef_score_full_values(self):
        """Test JEF score calculation with maximum values"""
        score = JEFScore(bv=1.0, bm=1.0, rt=1.0, fd=1.0)
        self.assertEqual(score.analyze(), 10.0)

    def test_analyze_jef_score_mixed_values(self):
        """Test JEF score calculation with mixed values"""
        score = JEFScore(bv=0.5, bm=0.6, rt=0.7, fd=0.8)
        expected = round(10 * (
            0.25 * 0.5 +  # bv weight * bv value
            0.15 * 0.6 +  # bm weight * bm value
            0.30 * 0.7 +  # rt weight * rt value
            0.30 * 0.8    # fd weight * fd value
        ), 2)
        self.assertEqual(score.analyze(), expected)

    def test_weights_sum_to_one(self):
        """Test that weights sum to 1.0"""
        total_weight = sum(JEFScore._WEIGHTS.values())
        self.assertEqual(total_weight, 1.0)

    def test_input_validation(self):
        """Test that invalid inputs are clamped appropriately"""
        score = JEFScore(bv=1.5, bm=-0.5, rt=2.0, fd=-1.0)
        self.assertEqual(score.bv, 1.0)
        self.assertEqual(score.bm, 0.0)
        self.assertEqual(score.rt, 1.0)
        self.assertEqual(score.fd, 0.0)


    def test_update_attr_valid_floats(self):
        """Test updating attributes with valid float values"""
        score = JEFScore(bv=0.1, bm=0.1, rt=0.1, fd=0.1)
        score.update_attr(bv=0.5, bm=0.6, rt=0.7, fd=0.8)
        self.assertEqual(score.bv, 0.5)
        self.assertEqual(score.bm, 0.6)
        self.assertEqual(score.rt, 0.7)
        self.assertEqual(score.fd, 0.8)


    def test_update_attr_non_float_values(self):
        """Test that non-float values are ignored"""
        score = JEFScore(bv=0.1, bm=0.1, rt=0.1, fd=0.1)
        score.update_attr(bv="0.5", bm=1, rt=True, fd=[0.8])
        self.assertEqual(score.bv, 0.1)  # Should remain unchanged
        self.assertEqual(score.bm, 0.1)  # Should remain unchanged
        self.assertEqual(score.rt, 0.1)  # Should remain unchanged
        self.assertEqual(score.fd, 0.1)  # Should remain unchanged


    def test_update_attr_clamping(self):
        """Test that values are properly clamped"""
        score = JEFScore()
        score.update_attr(bv=1.5, bm=-0.5, rt=2.0, fd=-1.0)
        self.assertEqual(score.bv, 1.0)  # Should clamp to 1.0
        self.assertEqual(score.bm, 0.0)  # Should clamp to 0.0
        self.assertEqual(score.rt, 1.0)  # Should clamp to 1.0
        self.assertEqual(score.fd, 0.0)  # Should clamp to 0.0


    def test_update_attr_invalid_keys(self):
        """Test that invalid keys are ignored"""
        score = JEFScore(bv=0.5, bm=0.5, rt=0.5, fd=0.5)
        score.update_attr(invalid_key=1.0, bv=0.7, another_invalid=2.0)
        self.assertEqual(score.bv, 0.7)  # Should update
        self.assertEqual(score.bm, 0.5)  # Should remain unchanged
        self.assertEqual(score.rt, 0.5)  # Should remain unchanged
        self.assertEqual(score.fd, 0.5)  # Should remain unchanged
        # Verify no new attributes were added
        self.assertFalse(hasattr(score, 'invalid_key'))
        self.assertFalse(hasattr(score, 'another_invalid'))


    def test_update_attr_empty_update(self):
        """Test update with no parameters"""
        score = JEFScore(bv=0.5, bm=0.5, rt=0.5, fd=0.5)
        original_values = {
            'bv': score.bv,
            'bm': score.bm,
            'rt': score.rt,
            'fd': score.fd
        }
        score.update_attr()
        self.assertEqual(score.bv, original_values['bv'])
        self.assertEqual(score.bm, original_values['bm'])
        self.assertEqual(score.rt, original_values['rt'])
        self.assertEqual(score.fd, original_values['fd'])


    def test_update_attr_partial_update(self):
        """Test updating only some attributes"""
        score = JEFScore(bv=0.5, bm=0.5, rt=0.5, fd=0.5)
        score.update_attr(bv=0.8, fd=0.9)
        self.assertEqual(score.bv, 0.8)  # Should update
        self.assertEqual(score.bm, 0.5)  # Should remain unchanged
        self.assertEqual(score.rt, 0.5)  # Should remain unchanged
        self.assertEqual(score.fd, 0.9)  # Should update



if __name__ == '__main__':
    unittest.main()
