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
```

### Running a local DB

Requires Docker CLI and an installation of PostgresQL on your machine.

Go into the `schema-migrations` directory and make the local DB script
executable:

```bash
$ cd schema-migrations/ && chmod +x local_cali_platform_db_setup.sh
```

Run the script:

```bash
$ ./local_cali_platform_db_setup.sh -d
```

Run it with `-h` to see the help:

```bash
$ ./local_cali_platform_db_setup.sh -h
USAGE: ./local_cali_platform_db_setup.sh [ARGS]

 -h                                    Show this help message
 -d                                    Build Calibration Platform container and run in background
 -f                                    Optionally copy the seed file to container and insert records
 -s                                    Clean up the Calibration Platform container
```


### Running the Flask API locally

From top of the project:

```bash
$ flask --app lv_calibration_platform.api.app run --debug
```


# Serverless Framework AWS Python Example

We use serverless in the higher (dev, prod) environments. See Serverless's AWS
Python example [here](https://www.serverless.com/examples/aws-python).
