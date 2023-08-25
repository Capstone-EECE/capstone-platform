# capstone-platform

## Developer Setup

### Installation

The `pyproject.toml` configures the Python package. Recommended to make and
activate a virtual environment for local development with something like
`python -m venv env` and activate it. Then just install with:

```bash
$ pip install -e .[dev]
```

Leave out the `[dev]` if you just want to install the package and none of the
local development dependencies.

#### pre-commit
You will need to get your pre-commit hooks installed:
```bash
$ pre-commit install