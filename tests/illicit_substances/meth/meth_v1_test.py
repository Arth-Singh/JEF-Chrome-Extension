import unittest
from jef.meth import score_v1


class MethV1Test(unittest.TestCase):
    def test_score(self):
        with open('./tests/illicit_substances/meth/meth_recipe_95.txt', 'r') as file:
            content = file.read()
            res = score_v1(content)
            self.assertEqual(res["score"], 10.5)


if __name__ == '__main__':
    unittest.main()