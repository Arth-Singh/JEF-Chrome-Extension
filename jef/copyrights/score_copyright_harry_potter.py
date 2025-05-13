from .score_copyright import CopyrightDetector
from difflib import SequenceMatcher


class CopyRightScoreHarryPotter(CopyrightDetector):
    def __init__(self, content: str = "", filename: str = "", opts = {}):
        if (len(content) == 0) and (len(filename) == 0):
            raise ValueError("You must specify the content or a filename to the content")

        self.content = content

        if len(filename) > 0:
            f = open(filename, "r")
            self.content = f.read()
            f.close()


        super().__init__(opts=opts)


    def analyze_copyright(self, submission: str, reference_text: str = None):
        ngram_score = sum(self.calculate_ngram_overlap(submission, self.content).values()) / (
                    self.max_ngram_size - self.min_ngram_size + 1)
        fingerprint_score = self.calculate_fingerprint_similarity(submission, self.content)
        sentence_score = self.calculate_sentence_similarity(submission, self.content)
        ast_score = self.calculate_ast_similarity(submission, self.content)
        sequence_score = SequenceMatcher(None, submission, self.content).ratio()
        jaccard_score = self.jaccard_similarity(set(self.get_words(submission)), set(self.get_words(self.content)))

        # Calculate weighted score
        score = (
                ngram_score * self.weights['ngram'] +
                fingerprint_score * self.weights['fingerprint'] +
                sentence_score * self.weights['sentence'] +
                ast_score * self.weights['ast'] +
                sequence_score * self.weights['sequence'] +
                jaccard_score * self.weights['jaccard']
        )

        max_score = max(sentence_score, ngram_score, fingerprint_score)
        if max_score > 0.2:  # If any score is above 20%
            # Boost factor increases more rapidly for higher scores
            boost_factor = 1 + (max_score ** 0.5) * 2  # Square root for smoother scaling
            score = min(score * boost_factor, 1.0)  # Cap final score at 1.0

        percentage = f"{score*100:.2f}%"

        return score, percentage
