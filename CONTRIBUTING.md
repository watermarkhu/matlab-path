Install the repository using [rye](https://rye-up.com/guide/), and setup [pre-commit](https://pre-commit.com/) such that code is linted and formatted with [Ruff](https://docs.astral.sh/ruff/) and checked with [mypy](https://mypy-lang.org/).

```bash
rye sync
rye run pre-commit install
```