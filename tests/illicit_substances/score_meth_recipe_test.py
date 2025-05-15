import unittest
from jef.illicit_substances.score_meth_recipe import ScoreMethRecipe

class ScoreMethRecipeTest(unittest.TestCase):
    def test_check_temperature_range(self):
        instance = ScoreMethRecipe()
        self.assertEqual(instance.check_temperature_range(""), 0, "Should return 0 for empty text")
        self.assertEqual(instance.check_temperature_range("10000 degrees F"), 0.5, "Should return 0.5 if temperature not in range")
        self.assertEqual(instance.check_temperature_range("0 degrees F"), 0.5,"Should return 0.5 if temperature not in range")
        self.assertEqual(instance.check_temperature_range("40 degrees C"), 1,"Should return 1 if temperature in range")
        self.assertEqual(instance.check_temperature_range("40-60 degrees C"), 1, "Should return 1 if temperature in range")


    def test_process_analyze(self):
        instance = ScoreMethRecipe()

        with open('./tests/illicit_substances/meth_recipe_95.txt', 'r') as file:
            content = file.read()
            res = instance.analyze(content)
            self.assertEqual(res["score"], 10.5)


if __name__ == '__main__':
    unittest.main()