from jef.helpers import get_latest_score_version
from jef.types import ScoreType
from jef.harmful_substances import nerve_agent


def score(recipe_text: str, show_matches: bool = False) -> ScoreType:
    '''
    method to call the latest version of score_v1 in the Harmful Substances Nerve Agent submodule
    '''
    recent_score_version = get_latest_score_version(dirname="jef.harmful_substances.nerve_agent")
    print(f'executing nerve agent {recent_score_version}')
    func = getattr(nerve_agent, recent_score_version)

    return func(
        recipe_text=recipe_text,
        show_matches=show_matches,
    )