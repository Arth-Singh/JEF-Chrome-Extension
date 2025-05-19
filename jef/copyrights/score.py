from jef.helpers import get_latest_score_version
from jef.types import CopyrightScoreType
from jef import copyrights


def score(submission: str, reference: str = "", min_ngram_size: int = 3, max_ngram_size: int = 7) -> CopyrightScoreType:
    '''
    method to call the latest version of score_v1 in the copyrights submodule
    '''
    recent_score_version = get_latest_score_version(dirname="jef.copyrights")
    print(f'executing copyrights {recent_score_version}')
    func = getattr(copyrights, recent_score_version)

    return func(submission=submission,
                reference=reference,
                min_ngram_size=min_ngram_size,
                max_ngram_size=max_ngram_size)