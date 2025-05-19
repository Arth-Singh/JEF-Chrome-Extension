import unittest
import json
import jef
from jef import tiananmen

class TiananmenScoreTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.chinese_censorship.tiananmen")
        self.assertTrue(score_file_name == "score_v1")


    def test_shortcut_function(self):
        with open('tests/chinese_censorship/tiananmen/tiananmen_text.json', 'r') as f:
            data = json.load(f)

            for entry in data:
                res = tiananmen.score(entry['text'], False, entry['overrideFlags'])
                self.assertEqual(res["score"], entry['score'], entry['text'])
                self.assertTrue(isinstance(res["score"], float))
                self.assertTrue(isinstance(res["percentage"], float))

if __name__ == '__main__':
    unittest.main()
