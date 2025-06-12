# jef/__init__.py

import tomllib
from pathlib import Path

from . import chinese_censorship
from . import copyrights
from . import harmful_substances
from . import illicit_substances
from . import score_algos


def _get_version():
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError):
        return "unknown"


calculator = score_algos.calculator
score = score_algos.score
__call__ = score
__version__ = _get_version()
