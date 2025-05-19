# Changelog

All notable changes to this project will be documented in this file.


## [0.1.0] - 2025-05-15

### Added
- Initial release
- The initial scoring classes: 
```
    ScoreTiananmen
    CopyrightDetector
    CopyRightScoreHarryPotter
    ScoreAgent110Recipe
    ScoreMethRecipe
    JEFScore
```

### Changed
- Initialize release

### Fixed
- Initialize release

## [0.1.1] - 2025-05-19

### ADDED
- new score function which always take the latest score_vx variant of a scoring algo to be used

### CHANGED
- classes for the various individual scoring algo, and jef scoring algo has been removed
- scoring algos are now imported as modules, and can be used by calling score
- better abstraction of utility functions and scoring functions
