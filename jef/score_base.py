from jef.types import ScoreType

class ScoreBase:
    def analyze(self, **kwargs) -> ScoreType:
        """
            Base function to analyze the score, required for all classes that inherit from this class.
        """
        raise NotImplemented