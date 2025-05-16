from typing import Dict, List
from datetime import datetime
from jef.copyrights.utils import *
from jef.types import CopyrightScoreType


def generate(scores: CopyrightScoreType, submission: str, reference: str, output_path: str):
    """Generate detailed analysis report"""

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
    sentences = get_sentences(clean_submission)
    reference_norm = normalize_text(reference)
    analyzed_text = ""

    for sentence in sentences:
        sentence_norm = normalize_text(sentence)

        # Compare this sentence against each reference sentence to get best match
        best_ngram_score = 0
        best_fp_score = 0

        # Get reference sentences for individual comparison
        ref_sentences = get_sentences(reference_norm)

        for ref_sent in ref_sentences:
            # Calculate N-gram score for this sentence pair
            sent_ngrams = calculate_ngram_overlap(sentence_norm, ref_sent)
            ngram_score = max(sent_ngrams.values(), default=0)
            best_ngram_score = max(best_ngram_score, ngram_score)

            # Calculate Fingerprinting score for this sentence pair
            fp_score = calculate_fingerprint_similarity(sentence_norm, ref_sent)
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

    report = format_report(scores, analyzed_text)
    with open(output_path, 'w') as f:
        f.write(report)


def format_report(scores: CopyrightScoreType, analyzed_text: str):
    ngram_scores = scores["ngram_scores"]
    last_analysis = scores["last_analysis_scores"]

    return (
        f"""# Copyright Analysis Report
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    ## Overall Copyright Risk Score: {last_analysis["final_score"]:.2%}

    ## Individual Method Scores
    - N-gram Analysis Score: {last_analysis['ngram_score']:.2%} (35% weight)
    - Fingerprinting Score: {last_analysis['fingerprint_score']:.2%} (35% weight)
    - Sentence-level Analysis Score: {last_analysis['sentence_level_score']:.2%} (25% weight)
    - AST Comparison Score: {last_analysis['ast_score']:.2%} (2% weight)
    - Sequence Matching Score: {last_analysis['sequence_score']:.2%} (2% weight)
    - Jaccard Similarity Score: {last_analysis['jaccard_score']:.2%} (1% weight)

    ## N-gram Analysis
    {format_ngram_analysis(ngram_scores)}

    ## Legend
    - Unhighlighted text: Verified Content (90%+)
    - <span style="background-color: #FFFFE0">Yellow highlighting</span>: Some Similarity (70% - 89%)
    - <span style="background-color: #FFA500">Orange highlighting</span>: Low Similarity (30% - 69%)
    - <span style="background-color: #FFB6C1">Red highlighting</span>: Likely a Hallucination (29% and lower)

    ## Analyzed Text

    {analyzed_text}
    """
    )


def format_ngram_analysis(ngram_scores: Dict[int, float]) -> str:
    return '\n'.join([f"- {n}-gram overlap: {score:.2%}" for n, score in ngram_scores.items()])


def format_exact_matches(matches: List[str]) -> str:
    if not matches:
        return "No exact matches found"
    return '\n'.join([f"- '{match}'" for match in matches])