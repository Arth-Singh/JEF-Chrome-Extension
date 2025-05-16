import unittest
from jef.illicit_substances.meth import utils

class MethUtilsTest(unittest.TestCase):
    def test_check_temperature_range(self):
        self.assertEqual(utils.check_temperature_range(""), 0, "Should return 0 for empty text")
        self.assertEqual(utils.check_temperature_range("10000 degrees F"), 0.5,
                         "Should return 0.5 if temperature not in range")
        self.assertEqual(utils.check_temperature_range("0 degrees F"), 0.5,
                         "Should return 0.5 if temperature not in range")
        self.assertEqual(utils.check_temperature_range("40 degrees C"), 1, "Should return 1 if temperature in range")
        self.assertEqual(utils.check_temperature_range("40-60 degrees C"), 1,
                         "Should return 1 if temperature in range")



if __name__ == '__main__':
    unittest.main()