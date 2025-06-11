# Contributing to 0din JEF
Thank you for considering contributing to this project. Our mission is to make this tool an industry standard, and with your contributions, we are one closer to achieving our goals.

## Getting Started

### Development Environment

We recommend using Python 3.8 or newer. The following tools are required:

- Python 3.12+
- pip
- git


### Fork & Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```
git clone https://github.com/your-repo/0din-JEF.git
cd 0din-JEF
git remote add upstream https://github.com/0din-ai/0din-JEF.git
```

### Virtual Environment

We strongly recommend using a virtual environment:

```
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

### Install Dependencies
```
pip install -e ".[dev]"
```

### How to use
This is a module so once you install it, you would have to build some random python file 
that imports the modules you want to execute to test them

You can also build test files and do the same thing.

### Running Tests
```
pip install .
pytest ./tests
```

## Types of Contributions you can do

### Code Contributions
- New scoring algorithms
- Performance improvements
- Bug fixes
- Documentation improvements
- Fixing issues

### Documentation
Sphynx is used in the workflow to generate new api documentations whenever a release happens
so please use the Google Docstring format to ensure changes are reflected on automatic generated
docs

### Bug Reports
- Use the GitHub issue template
- Include steps to reproduce
- Provide system information
- Include relevant logs or error messages

### Adding New Scoring Algorithms
1. Create a new module in the appropriate category (e.g., `jef/copyrights/`)
2. Follow the naming convention: `score_v1.py`, `score_v2.py`, etc.
3. Include comprehensive tests in the `tests/` directory
4. Update documentation with usage examples

### Testing Your Changes

This is a module, so to test your changes:

1. Create a test Python file that imports the modules you want to test
2. Use the existing test files as examples
3. Ensure your tests cover edge cases and expected behavior
4. If tests fail, PRs cannot be merged.