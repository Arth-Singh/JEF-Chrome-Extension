from jef.helpers import get_latest_score_version
from jef import score_algos


def score(bv:float=0.0, bm:float=0.0, rt:float=0.0, fd:float=0.0):
    '''
    method to call the latest version of jef_score
    '''
    recent_score_version = get_latest_score_version(dirname="jef.score_algos", match=r'^score_v(\d+)\.py$')
    print(f'executing jef score {recent_score_version}')

    func = getattr(score_algos, recent_score_version)
    return func(bv=bv, bm=bm, rt=rt, fd=fd)


__call__ = score