import logging

import yaml
from sqlalchemy import create_engine, URL
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from src.models import Base, Transaction

logger = logging.getLogger("DbManager")
CONFIG_PATH = "src/configs/db_config.yaml"
DBMS = "Postgres"

with open(CONFIG_PATH, "r", encoding="utf_8") as file:
    config = yaml.safe_load(file)
url_object = URL.create(
    "postgresql",
    host=config[DBMS]["host"],
    username=config[DBMS]["user"],
    password=config[DBMS]["password"],
    database=config[DBMS]["database"]
)

engine = create_engine(url_object)

if not database_exists(engine.url):
    logger.warning(f"Database {config[DBMS]['database']} doesn't exist")
    create_database(engine.url)
    logger.warning(f"Database {config[DBMS]['database']} created")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_transaction(amount, category, date=None, description=""):
    session = Session()
    try:
        transaction = Transaction(amount=amount, category=category, date=date, description=description)
        session.add(transaction)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_transactions():
    session = Session()
    try:
        transactions = session.query(Transaction).all()
        return transactions
    finally:
        session.close()
