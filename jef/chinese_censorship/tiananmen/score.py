from jef.chinese_censorship import tiananmen
from jef.types import ScoreType
from jef.helpers import get_latest_score_version
from typing import List

def score(input_text: str, show_matches: bool = False, override_flags: List[str] = None) -> ScoreType:
    '''
    This method invokes the latest version of score_v1 in the Chinese Censorship Tiananmen submodule
    '''
    recent_score_version = get_latest_score_version(dirname="jef.chinese_censorship.tiananmen")
    print(f'executing tiananmen {recent_score_version}')

    func = getattr(tiananmen, recent_score_version)
    return func(input_text=input_text,
               show_matches=show_matches,
               override_flags=override_flags)


