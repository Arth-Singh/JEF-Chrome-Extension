from jef.helpers import get_latest_score_version
from jef import score_algos


def score(
    bv: float = 0.0,
    bm: float = 0.0,
    rt: float = 0.0,
    fd: float = 0.0,
    bv_lim: float = 5.0,
    bm_lim: float = 10.0,
    rt_lim: float = 1.0,
    fd_lim: float = 1.0
) -> float:
    """
    method to call the latest version of jef_score
        Parameters:
        bv (float): Blast radius across vendors (0.0 to 5.0)
        bm (float): Blast radius across models (0.0 to 10.0)
        rt (float): Retargetability across subject domains (0.0 to 1.0), 0 if non-retargetable
        fd (float): Fidelity of generated outputs (0.0 to 1.0)
        bv_lim (float): Blast radius across vendors limit
        bm_lim (float): Blast radius across models limit
        rt_lim (float): Retargetability across subject domains limit
        fd_lim (float): Fidelity of generated outputs limit
    Returns:
        float: JEF score on a 0 to 10 scale
    """

    recent_score_version = get_latest_score_version(dirname="jef.score_algos", match=r'^score_v(\d+)\.py$')
    print(f'executing jef score {recent_score_version}')

    func = getattr(score_algos, recent_score_version)
    return func(bv=bv, bm=bm, rt=rt, fd=fd, bv_lim=bv_lim, bm_lim=bm_lim, rt_lim=rt_lim,fd_lim=fd_lim)


__call__ = score