# jef/__init__.py

from . import chinese_censorship
from . import copyrights
from . import harmful_substances
from . import illicit_substances
from . import score_algos


score = score_algos.score
__call__ = score