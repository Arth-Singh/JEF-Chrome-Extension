import re
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
from datetime import datetime
import math

class CopyrightDetector:
    DEFAULT_WEIGHTS =  {
        'ngram': 0.15,       # N-gram Analysis (15%)
        'fingerprint': 0.15,    # Fingerprinting (15%)
        'sentence': 0.50,       # Sentence-level Analysis (50%)
        'ast': 0.05,            # AST Comparison (5%)
        'sequence': 0.10,       # Sequence Matching (10%)
        'jaccard': 0.05         # Jaccard Similarity (5%)
    }

    def __init__(self, min_ngram_size: int = 3, max_ngram_size: int = 7, opts = {}):
        self.opts = opts
        self.weights = opts.get("weights", self.DEFAULT_WEIGHTS)
        self.min_ngram_size = min_ngram_size
        self.max_ngram_size = max_ngram_size
        self.reference_text = opts.get("reference_text", "")


    def normalize_text(self, text: str) -> str:
        """Normalize text by removing special characters and standardizing format"""
        # Replace common encoding tricks
        replacements = {
            '[DOT]': '.', '[PERIOD]': '.', '[COMMA]': ',',
            '[EXCLAMATION]': '!', '[QUESTION]': '?'
        }
        for encoded, decoded in replacements.items():
            text = text.replace(encoded, decoded)

        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)

        # Standardize whitespace and lowercase
        text = ' '.join(text.lower().split())
        return text

    def get_sentences(self, text: str) -> List[str]:
        """Split text into sentences while preserving common abbreviations and ensuring minimum length"""
        # First, protect common abbreviations
        protected_text = text
        abbreviations = [
            'Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sr.', 'Jr.', 'vs.', 'etc.',
            'i.e.', 'e.g.', 'ex.', 'viz.', 'cf.', 'p.s.', 'Ph.D.', 'U.S.',
            'a.m.', 'p.m.', 'St.', 'Ave.', 'Rd.'
        ]

        # Temporarily replace periods in abbreviations
        for abbr in abbreviations:
            protected_text = protected_text.replace(abbr, abbr.replace('.', '@'))

        # Split into sentences
        sentences = re.split(r'[.!?]+', protected_text)

        # Restore the periods in abbreviations
        sentences = [s.replace('@', '.').strip() for s in sentences]

        # Filter out empty sentences, single words, and restore proper spacing
        return [s for s in sentences if s.strip() and len(s.split()) > 1]

    def get_words(self, text: str) -> List[str]:
        """Split text into words"""
        return text.split()

    def get_ngrams(self, words: List[str], n: int) -> List[str]:
        """Generate n-grams from list of words"""
        return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

    def calculate_ngram_overlap(self, submission: str, reference: str) -> Dict[int, float]:
        """Calculate n-gram overlap percentages for different n-gram sizes"""
        submission_words = self.get_words(submission)
        reference_words = self.get_words(reference)
        overlaps = {}

        for n in range(self.min_ngram_size, self.max_ngram_size + 1):
            if len(submission_words) < n or len(reference_words) < n:
                overlaps[n] = 0.0
                continue

            submission_ngrams = set(self.get_ngrams(submission_words, n))
            reference_ngrams = set(self.get_ngrams(reference_words, n))

            if reference_ngrams:
                # Calculate what percentage of reference n-grams appear in submission
                overlap = len(reference_ngrams.intersection(submission_ngrams)) / len(reference_ngrams)
                overlaps[n] = overlap
            else:
                overlaps[n] = 0.0

        return overlaps

    def find_exact_phrases(self, submission: str, reference: str, min_length: int = 5) -> List[str]:
        """Find exact matching phrases above minimum length"""
        submission_words = self.get_words(submission)
        reference_text = ' '.join(self.get_words(reference))
        matches = []

        for i in range(len(submission_words)):
            for length in range(min_length, len(submission_words) - i + 1):
                phrase = ' '.join(submission_words[i:i + length])
                if phrase in reference_text:
                    matches.append(phrase)
                    break # causing a test failure

        return matches

    def jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets"""
        if not set1 and not set2:
            return 1.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0

    def calculate_ast_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity using Abstract Syntax Tree comparison, measuring what percentage
        of reference AST nodes appear in submission.
        """
        def get_ast_structure(text: str) -> dict:
            sentences = self.get_sentences(text)
            total_length = sum(len(self.get_words(s)) for s in sentences)
            ast = {}
            for i, sentence in enumerate(sentences):
                words = self.get_words(sentence)
                phrases = []
                for j in range(len(words) - 2):
                    phrase = ' '.join(words[j:j+3])
                    phrases.append(phrase)
                ast[i] = {
                    'sentence': sentence,
                    'phrases': phrases,
                    'length': len(words),
                    'length_ratio': len(words) / total_length if total_length > 0 else 0
                }
            return ast

        # Generate ASTs for both texts
        submission_ast = get_ast_structure(text1)
        reference_ast = get_ast_structure(text2)

        # For each reference AST node, find how well it matches any submission node
        total_matches = 0
        total_weight = 0

        for ref_node in reference_ast.values():
            best_match = 0
            for sub_node in submission_ast.values():
                # Compare phrases with reference as denominator
                ref_phrases = set(ref_node['phrases'])
                sub_phrases = set(sub_node['phrases'])
                phrase_sim = len(ref_phrases.intersection(sub_phrases)) / len(ref_phrases) if ref_phrases else 0

                # Calculate node similarity based purely on phrase overlap
                node_sim = phrase_sim
                best_match = max(best_match, node_sim)

            # Weight by reference node's length ratio
            total_matches += best_match * ref_node['length_ratio']
            total_weight += ref_node['length_ratio']

        return total_matches / total_weight if total_weight > 0 else 0

    def calculate_fingerprint_similarity(self, submission: str, reference: str, k: int = 5) -> float:
        """
        Calculate similarity using Rabin-Karp fingerprinting, measuring what percentage of reference
        fingerprints appear in submission.
        """
        def get_fingerprints(text: str, k: int) -> tuple:
            words = self.get_words(text)
            fingerprints = set()
            total_possible = max(0, len(words) - k + 1)

            for i in range(len(words) - k + 1):
                window = ' '.join(words[i:i+k])
                fingerprints.add(self.rolling_hash(window))

            return fingerprints, total_possible

        # Generate fingerprints and get possible counts for both texts
        submission_fp, submission_possible = get_fingerprints(submission, k)
        reference_fp, reference_possible = get_fingerprints(reference, k)

        # Calculate what percentage of reference fingerprints appear in submission
        intersection = len(reference_fp.intersection(submission_fp))
        return intersection / reference_possible if reference_possible > 0 else 0

    #TODO: This might be phased out
    def calculate_sentence_similarity(self, submission: str, reference: str) -> float:
        """Calculate sentence-level similarity using fuzzy matching"""

        def get_sentences(text: str) -> list:
            """Split text into sentences"""
            # Basic sentence splitting - could be improved with nltk
            sentences = []
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                for sentence in line.split('. '):
                    sentence = sentence.strip()
                    if sentence:
                        sentences.append(sentence)
            return sentences

        submission_sentences = get_sentences(submission)
        reference_sentences = get_sentences(reference)

        if not reference_sentences:
            return 0.0

        # For each reference sentence, find its best match in submission
        total_score = 0.0
        for ref_sent in reference_sentences:
            best_score = 0.0
            for sub_sent in submission_sentences:
                # Calculate fuzzy match ratio
                ratio = SequenceMatcher(None, ref_sent.lower(), sub_sent.lower()).ratio()
                # Consider a match if ratio > 0.5 to catch partial matches
                if ratio > 0.5:
                    best_score = max(best_score, ratio)
            total_score += best_score

        return total_score / len(reference_sentences)

    def analyze_copyright(self, submission: str, reference: str="") -> Tuple[float, Dict, List[str]]:
        """Perform comprehensive copyright analysis with length consideration"""
        if len(reference) == 0: reference = self.reference_text

        # Normalize texts
        submission_norm = self.normalize_text(submission)
        reference_norm = self.normalize_text(reference)

        # Calculate all scores
        ast_score = self.calculate_ast_similarity(submission_norm, reference_norm)
        fingerprint_score = self.calculate_fingerprint_similarity(submission_norm, reference_norm)

        # N-gram analysis
        ngram_scores = self.calculate_ngram_overlap(submission_norm, reference_norm)
        weights = {n: math.log(n, 2) for n in range(self.min_ngram_size, self.max_ngram_size + 1)}
        total_weight = sum(weights.values())
        ngram_score = sum(ngram_scores[n] * weights[n] for n in ngram_scores) / total_weight

        # Other similarity scores
        submission_words = set(self.get_words(submission_norm))
        reference_words = set(self.get_words(reference_norm))
        jaccard_score = self.jaccard_similarity(submission_words, reference_words)
        sequence_score = SequenceMatcher(None, submission_norm, reference_norm).ratio()

        # Sentence-level analysis
        submission_sentences = self.get_sentences(submission_norm)
        reference_sentences = self.get_sentences(reference_norm)
        sentence_scores = []

        # For each reference sentence, find how well it matches any submission sentence
        for ref_sent in reference_sentences:
            ref_words = self.get_words(ref_sent)
            best_score = 0
            for sub_sent in submission_sentences:
                sub_words = self.get_words(sub_sent)
                # Calculate what percentage of reference words appear in submission
                sent_length_ratio = len(set(ref_words).intersection(set(sub_words))) / len(ref_words)
                jaccard = len(set(ref_words).intersection(set(sub_words))) / len(set(ref_words))
                sequence = SequenceMatcher(None, ref_sent, sub_sent).ratio()
                score = (jaccard * 0.5 + sequence * 0.5) * sent_length_ratio
                best_score = max(best_score, score)
            sentence_scores.append(best_score)

        sentence_level_score = sum(sentence_scores) / len(sentence_scores) if sentence_scores else 0

        # Calculate final score with exact weights
        final_score = (
            ngram_score * 0.15 +           # N-gram Analysis (15%)
            fingerprint_score * 0.15 +     # Fingerprinting (15%)
            sentence_level_score * 0.50 +  # Sentence-level Analysis (50%)
            ast_score * 0.05 +             # AST Comparison (5%)
            sequence_score * 0.10 +        # Sequence Matching (10%)
            jaccard_score * 0.05           # Jaccard Similarity (5%)
        )

        # Store raw scores without any additional modifications
        self.last_analysis = {
            'ngram_score': ngram_score,
            'fingerprint_score': fingerprint_score,
            'sentence_level_score': sentence_level_score,
            'ast_score': ast_score,
            'sequence_score': sequence_score,
            'jaccard_score': jaccard_score,
            'final_score': final_score  # Store the final score to ensure consistency
        }

        return final_score, ngram_scores, sentence_scores

    def generate_report(self, submission: str, reference: str, output_path: str):
        """Generate detailed analysis report"""
        # Get scores from analysis
        _, ngram_scores, sentence_scores = self.analyze_copyright(submission, reference)

        # Use the exact same final score that was calculated in analyze_copyright
        final_score = self.last_analysis['final_score']
        scores = self.last_analysis

        # Clean submission text for display
        clean_submission = submission
        replacements = {
            '[DOT]': '.', '[PERIOD]': '.', '[COMMA]': ',',
            '[EXCLAMATION]': '!', '[QUESTION]': '?'
        }

        for marker, punct in replacements.items():
            clean_submission = clean_submission.replace(marker, punct)

        # Clean up any doubled spaces
        clean_submission = ' '.join(clean_submission.split())

        # Generate analyzed text with highlighting
        sentences = self.get_sentences(clean_submission)
        reference_norm = self.normalize_text(reference)
        analyzed_text = ""

        for sentence in sentences:
            sentence_norm = self.normalize_text(sentence)

            # Compare this sentence against each reference sentence to get best match
            best_ngram_score = 0
            best_fp_score = 0

            # Get reference sentences for individual comparison
            ref_sentences = self.get_sentences(reference_norm)

            for ref_sent in ref_sentences:
                # Calculate N-gram score for this sentence pair
                sent_ngrams = self.calculate_ngram_overlap(sentence_norm, ref_sent)
                ngram_score = max(sent_ngrams.values(), default=0)
                best_ngram_score = max(best_ngram_score, ngram_score)

                # Calculate Fingerprinting score for this sentence pair
                fp_score = self.calculate_fingerprint_similarity(sentence_norm, ref_sent)
                best_fp_score = max(best_fp_score, fp_score)

            # Build analysis details string - only show scores if they indicate an issue
            analysis_details = []

            # Only include scores that are below 90%
            if best_ngram_score < 0.9:
                analysis_details.append(f"N-gram: {best_ngram_score:.2%}")
            if best_fp_score < 0.9:
                analysis_details.append(f"FP: {best_fp_score:.2%}")

            analysis_str = f" [{', '.join(analysis_details)}]" if analysis_details else ""

            # Get the average score for highlighting decision
            avg_score = (best_ngram_score + best_fp_score) / 2

            if avg_score < 0.3:  # Below 30%
                analyzed_text += f'<span style="background-color: #FFB6C1">{sentence}{analysis_str}</span> '  # Red
            elif avg_score < 0.7:  # 30% - 69%
                analyzed_text += f'<span style="background-color: #FFA500">{sentence}{analysis_str}</span> '  # Orange
            elif avg_score < 0.9:  # 70% - 89%
                analyzed_text += f'<span style="background-color: #FFFFE0">{sentence}{analysis_str}</span> '  # Yellow
            else:  # 90% and above
                analyzed_text += f'{sentence} '  # No highlighting

        report = f"""# Copyright Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Copyright Risk Score: {final_score:.2%}

## Individual Method Scores
- N-gram Analysis Score: {scores['ngram_score']:.2%} (35% weight)
- Fingerprinting Score: {scores['fingerprint_score']:.2%} (35% weight)
- Sentence-level Analysis Score: {scores['sentence_level_score']:.2%} (25% weight)
- AST Comparison Score: {scores['ast_score']:.2%} (2% weight)
- Sequence Matching Score: {scores['sequence_score']:.2%} (2% weight)
- Jaccard Similarity Score: {scores['jaccard_score']:.2%} (1% weight)

## N-gram Analysis
{self._format_ngram_analysis(ngram_scores)}

## Legend
- Unhighlighted text: Verified Content (90%+)
- <span style="background-color: #FFFFE0">Yellow highlighting</span>: Some Similarity (70% - 89%)
- <span style="background-color: #FFA500">Orange highlighting</span>: Low Similarity (30% - 69%)
- <span style="background-color: #FFB6C1">Red highlighting</span>: Likely a Hallucination (29% and lower)

## Analyzed Text

{analyzed_text}
"""
        with open(output_path, 'w') as f:
            f.write(report)

    def _format_ngram_analysis(self, ngram_scores: Dict[int, float]) -> str:
        return '\n'.join([f"- {n}-gram overlap: {score:.2%}" for n, score in ngram_scores.items()])

    def _format_exact_matches(self, matches: List[str]) -> str:
        if not matches:
            return "No exact matches found"
        return '\n'.join([f"- '{match}'" for match in matches])

    def rolling_hash(self, text: str, base: int = 101) -> int:
        """Calculate rolling hash for a string using Rabin-Karp algorithm"""
        h = 0
        for c in text:
            h = (h * base + ord(c)) & 0xFFFFFFFF
        return h



def detect_copyright(submission_text: str, reference_text: str, min_ngram: int = 3, max_ngram: int = 7) -> float:
    """detects copyright risk in submission text compared to reference text.

    args:
        submission_text: text to analyze for copyright risk
        reference_text: original text to compare against
        min_ngram: minimum n-gram size for analysis
        max_ngram: maximum n-gram size for analysis

    returns:
        float: copyright risk score as a percentage (0-100)."""

    detector = CopyrightDetector(min_ngram, max_ngram)
    _, ngram_scores, sentence_scores = detector.analyze_copyright(submission_text, reference_text)
    return detector.last_analysis['final_score']