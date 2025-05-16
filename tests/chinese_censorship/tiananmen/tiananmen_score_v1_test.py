import unittest
import json
import jef
from jef.tiananmen import score_v1 as score

class TiananmenScoreV1Test(unittest.TestCase):
    def test_score(self):
        with open('tests/chinese_censorship/tiananmen/tiananmen_text.json', 'r') as f:
            data = json.load(f)

            for entry in data:
                res = score(entry['text'], False, entry['overrideFlags'])
                self.assertEqual(res["score"], entry['score'], entry['text'])
                self.assertTrue(isinstance(res["score"], float))
                self.assertTrue(isinstance(res["percentage"], float))


if __name__ == '__main__':
    unittest.main()
