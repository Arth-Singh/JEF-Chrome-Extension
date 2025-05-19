import unittest
import jef
from jef import meth


class MethTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.illicit_substances.meth")
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        with open('./tests/illicit_substances/meth/meth_recipe_95.txt', 'r') as file:
            content = file.read()
            res = meth.score(content)
            self.assertEqual(res["score"], 10.5)


if __name__ == '__main__':
    unittest.main()