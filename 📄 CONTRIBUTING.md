# Contributing to Zerix

## Branch Model
- `main` — stable, always releasable.
- `feat/*` — new features.
- `fix/*` — bug fixes.
- `security/*` — security fixes (private until patched).

## Commit Convention
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(policy): add weekly spending cap
fix(signer): handle timeout in Turnkey adapter
docs(readme): update quickstart
```

## Pull Requests
1. Fork & branch off `main`.
2. Add tests for behavior changes.
3. Make sure `pytest` and `pip-audit` pass.
4. Fill out the PR template (what, why, how it was tested).
5. At least 1 review from a maintainer.

## Test Gate
- Unit test coverage for `zerix/policy/` must be at least 90%.
- All PRs must pass CI: lint, type-check, test, security scan.

## Development Setup

```bash
git clone https://github.com/zerix-dev/zerix.git
cd zerix
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
