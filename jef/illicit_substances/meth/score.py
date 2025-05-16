from jef.helpers import get_latest_score_version
from jef.types import ScoreType
from jef.illicit_substances import meth
from typing import List


def score(recipe_text: str, show_matches: bool = False, override_temperature: bool = False,
            override_flags: List[str] = None) -> ScoreType:
    '''
    method to call the latest version of score_v1 in the illicit substances meth submodule
    '''
    recent_score_version = get_latest_score_version(dirname="jef.illicit_substances.meth")
    print(f'executing meth {recent_score_version}')
    func = getattr(meth, recent_score_version)

    return func(
        recipe_text=recipe_text,
        show_matches=show_matches,
        override_temperature=override_temperature,
        override_flags=override_flags
    )