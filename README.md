# capstone-platform

## Developer Setup

### Installation

The `pyproject.toml` configures the Python package. Recommended to make and
activate a virtual environment for local development with something like
`python -m venv env` and activate it. Then just install with:

```bash
$ pip install --upgrade pip

$ pip install -e .[dev]
```

Leave out the `[dev]` if you just want to install the package and none of the
local development dependencies.

#### pre-commit
You will need to get your pre-commit hooks installed:
```bash
$ pre-commit install
```

### Running a local DB

Requires Docker CLI and an installation of PostgresQL on your machine.

Go into the `schema-migrations` directory and make the local DB script
executable:

```bash
$ cd schema-migrations/ && chmod +x setup_local_db.sh
```

Run the script:

```bash
$ ./setup_local_db.sh -d
```

Run it with `-h` to see the help:

```bash
$ ./setup_local_db.sh -h
USAGE: ./setup_local_db.sh [ARGS]

 -h                                    Show this help message
 -d                                    Build Platform container and run in background
 -f                                    Copy the seed file to container and insert records
 -s                                    Clean up the Platform container
```


### Running the Flask API locally

From top of the project:

```bash
$ flask --app server.api.app run --debug
```


# Serverless Framework AWS Python Example

We use serverless in the higher (dev, prod) environments. See Serverless's AWS
Python example [here](https://www.serverless.com/examples/aws-python).
