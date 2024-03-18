Install the repository after cloning with [poetry](https://python-poetry.org/), and setup [pre-commit](https://pre-commit.com/) such that code is linted and formatted with [Ruff](https://docs.astral.sh/ruff/) and checked with [mypy](https://mypy-lang.org/).

```bash
pip install poetry
cd matlab-path
poetry install
pre-commit install
```