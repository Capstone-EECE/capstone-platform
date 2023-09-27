import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


def get_credentials() -> dict:
    return {
        "dbname": "capstone",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": 8501,
    }


db_engine = None
log = logging.getLogger(__name__)


def get_engine():
    global db_engine
    if db_engine is None:
        creds = get_credentials()
        log.info(
            "Connecting to database postgresql://%s:%s@%s:%s/%s",
            creds["user"],
            "*******",
            creds["host"],
            creds["port"],
            creds["dbname"],
        )
        db_engine = create_engine(
            URL.create(
                "postgresql",
                username=creds["user"],
                password=creds["password"],
                host=creds["host"],
                port=creds["port"],
                database=creds["dbname"],
            ),
        )
    return db_engine


def get_session_factory():
    return sessionmaker(bind=get_engine())
