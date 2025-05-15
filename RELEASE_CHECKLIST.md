# Release Checklist

## Pre-release
- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md with new version details
- [ ] Run all tests locally: `pytest`
- [ ] Build package locally to verify: `python -m build`
- [ ] Commit all changes: `git commit -am "Prepare for release X.Y.Z"`
- [ ] Push changes: `git push origin main`

## Create GitHub Release
- [ ] Go to GitHub repository → Releases → Draft a new release
- [ ] Create a new tag with the version (e.g., `v0.1.0`)
- [ ] Title the release with the version
- [ ] Add release notes from CHANGELOG.md. BE SPECIFIC PLEASE
- [ ] If pre-release, mark as "Pre-release"
- [ ] Publish release

## Post-release
- [ ] Verify the GitHub Actions workflow ran successfully
- [ ] Check PyPI to ensure the package was published
- [ ] Install the package from PyPI to verify: `pip install 0din-jef`
- [ ] Update documentation with new version details
- [ ] Announce release to users (if applicable)
