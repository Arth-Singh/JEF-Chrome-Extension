from jef.helpers import get_latest_score_version
from jef.copyrights import harry_potter
from jef.types import CopyrightScoreType


def score(submission: str, reference: str = "", min_ngram_size: int = 3, max_ngram_size: int = 7) -> CopyrightScoreType:
    '''
    method to call the latest version of score_v1 in the harry potter copyrights submodule
    '''
    recent_score_version = get_latest_score_version(dirname="jef.copyrights.harry_potter")
    print(f'executing harry potter copyrights {recent_score_version}')
    func = getattr(harry_potter, recent_score_version)

    return func(submission=submission,
                reference=reference,
                min_ngram_size=min_ngram_size,
                max_ngram_size=max_ngram_size)