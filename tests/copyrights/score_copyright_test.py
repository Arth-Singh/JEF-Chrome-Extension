import unittest
import tempfile
import os
from jef.copyrights.score_copyright import CopyrightDetector, detect_copyright

class CopyRightDetectorTest(unittest.TestCase):
    def setUp(self):
        self.instance = CopyrightDetector()

    def test_normalize_test(self):
        raw_text = "Hello[DOT] This is a test[EXCLAMATION] Visit example[PERIOD]com"
        expected = "hello. this is a test! visit example.com"
        self.assertEqual(self.instance.normalize_text(raw_text), expected)


    def test_get_sentences(self):
        text = "Dr. Smith went to the U.S. to California. It was sunny."
        sentences = self.instance.get_sentences(text)
        self.assertIn("Dr. Smith went to the U.S. to California", sentences)
        self.assertIn("It was sunny", sentences)

    def test_get_words(self):
        text = "this is a test"
        self.assertEqual(self.instance.get_words(text), ["this", "is", "a", "test"])

    def test_get_ngrams(self):
        words = ["this", "is", "a", "test"]
        expected = ["this is", "is a", "a test"]
        self.assertEqual(self.instance.get_ngrams(words, 2), expected)

    def test_calculate_ngram_overlap(self):
        sub = "the quick brown fox"
        ref = "the quick brown fox jumps"
        scores = self.instance.calculate_ngram_overlap(sub, ref)
        self.assertTrue(3 in scores)
        self.assertGreater(scores[3], 0)

    def test_find_exact_phrases(self):
        sub = "the quick brown fox jumps over the lazy dog"
        ref = "quick brown fox jumps"
        matches = self.instance.find_exact_phrases(sub, ref, min_length=3)

        self.assertTrue(any("quick brown fox jumps" in m for m in matches))

    def test_jaccard_similarity(self):
        set1 = {"a", "b", "c"}
        set2 = {"b", "c", "d"}
        expected = 2 / 4  # Intersection: 2, Union: 4
        self.assertAlmostEqual(self.instance.jaccard_similarity(set1, set2), expected)

    def test_calculate_ast_similarity(self):
        t1 = "The cat sat on the mat. It was quiet."
        t2 = "A cat sat on a rug. Everything was silent."
        sim = self.instance.calculate_ast_similarity(t1, t2)
        self.assertGreaterEqual(sim, 0)
        self.assertLessEqual(sim, 1)

    def test_calculate_fingerprint_similarity(self):
        sub = "the quick brown fox jumps over the lazy dog"
        ref = "quick brown fox jumps over lazy dog"
        sim = self.instance.calculate_fingerprint_similarity(sub, ref, k=3)
        self.assertGreater(sim, 0)

    def test_calculate_sentence_similarity(self):
        sub = "The fox jumps over the dog."
        ref = "A fox jumps over the lazy dog."
        score = self.instance.calculate_sentence_similarity(sub, ref)
        self.assertGreater(score, 0.5)

    def test_analyze(self):
        sub = "This is a test sentence. Another line follows."
        ref = "This is a test sentence. Something else."
        res  = self.instance.analyze(sub, ref)

        score = res["score"]
        ngrams = res["ngram_scores"]
        sent_scores = res["sentence_scores"]
        self.assertGreater(score, 0)
        self.assertGreater(ngrams[3], 0)
        self.assertGreater(sent_scores[0], 0)

    def test_generate_report(self):
        """Test report generation functionality"""
        submission = "This is a test sentence. This is unique content. This is copied exactly."
        reference = "Something different here. More unique text. This is copied exactly."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tf:
            report_path = tf.name

        try:
            self.instance.generate_report(submission, reference, report_path)

            # Verify report was created and contains expected sections
            with open(report_path, 'r') as f:
                report_content = f.read()

            self.assertIn("Copyright Analysis Report", report_content)
            self.assertIn("Overall Copyright Risk Score", report_content)
            self.assertIn("Individual Method Scores", report_content)
            self.assertIn("N-gram Analysis", report_content)
            self.assertIn("Legend", report_content)
            self.assertIn("Analyzed Text", report_content)
        finally:
            os.unlink(report_path)


if __name__ == '__main__':
    unittest.main()