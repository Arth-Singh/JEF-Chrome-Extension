import re
import importlib.resources
import os

def get_latest_score_version(dirname: str ="", match: str = r'^score_v(\d+)\.py$') -> str:
    pattern = re.compile(match)
    # Get the package directory
    package_dir = importlib.resources.files(dirname)
    all_files = os.listdir(package_dir)
    score_files = [f for f in all_files if pattern.match(f)]
    score_files.sort()
    if len(score_files) > 0 :
        return score_files[-1].split('.')[0]
    else:
        raise "Unable to find score latest score method"