import unittest
import json
from jef.chinese_censorship.score_tiananmen import ScoreTiananmen

class ScoreTiananmenTest(unittest.TestCase):
    def setUp(self):
        self.instance = ScoreTiananmen()

    def test_analyze(self):
        with open('tests/chinese_censorship/tiannanmen_text.json', 'r') as f:
            data = json.load(f)

            for entry in data:
                res = self.instance.analyze(entry['text'], True, entry['overrideFlags'])
                self.assertEqual(res["score"], entry['score'], entry['text'])
                self.assertTrue(isinstance(res["score"], float))
                self.assertTrue(isinstance(res["percentage"], float))


if __name__ == '__main__':
    unittest.main()