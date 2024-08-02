from datetime import datetime
from sqlalchemy import Column, Float, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL
from sqlalchemy_utils import database_exists, create_database
import logging
import yaml

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String)


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


def edit_transaction(transaction_id, amount=None, category=None, date=None, description=None):
    session = Session()
    try:
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            if amount is not None:
                transaction.amount = amount
            if category is not None:
                transaction.category = category
            if date is not None:
                transaction.date = date
            if description is not None:
                transaction.description = description
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_transaction(transaction_id):
    session = Session()
    try:
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            session.delete(transaction)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
