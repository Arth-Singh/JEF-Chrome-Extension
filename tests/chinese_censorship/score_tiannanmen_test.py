import unittest
import json
from jef.chinese_censorship.score_tiananmen import ScoreTiananmen

class ScoreTiananmenTest(unittest.TestCase):
    def setUp(self):
        self.instance = ScoreTiananmen()

    def test_process_text(self):
        with open('tests/chinese_censorship/tiannanmen_text.json', 'r') as f:
            data = json.load(f)
            for entry in data:
                score, matches, missing, percentage = self.instance.process_text(entry['text'], True, entry['overrideFlags'])
                print("\n", percentage, "%\n")
                self.assertEqual(score, entry['score'], entry['text'])


if __name__ == '__main__':
    unittest.main()