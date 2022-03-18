from datetime import datetime, timezone, timedelta, time
from time import sleep

from scheduler import Scheduler
import logging
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import database_exists, create_database

from db_models.base import metadata, BaseModel
from db_models.population import Population
from db_service import DbService

logger = logging.getLogger("scheduler")


class MembersGatherer:

    def __init__(self, telebot):
        self.telebot = telebot
        try:
            self.db_service = self.setup_db()
            logger.info("Scheduer prepared")
        except Exception as e:
            logger.error(e)
            raise e

    def setup_db(self):
        DB_USER = environ.get("DB_USER")
        DB_PASSWORD = environ.get("DB_PASS")
        DB_HOST = environ.get("DB_HOST")
        DB_NAME = environ.get("DB_NAME")
        SQLALCHEMY_DATABASE_URL = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        session_maker = sessionmaker(
            autocommit=False, bind=engine
        )
        if not database_exists(engine.url):
            create_database(engine.url)
        if not engine.dialect.has_schema(engine, metadata.schema):
            engine.execute(CreateSchema(metadata.schema))
        BaseModel.metadata.create_all(bind=engine)
        return DbService(session_maker)

    def gather_chat_members(self):
        amount = self.telebot.get_members_count()
        if amount is not None:
            new_population = Population(data=datetime.utcnow(), population=amount)
            with self.db_service.create(new_population):
                pass


def start_scheduler(telebot):
    gatherer = MembersGatherer(telebot)
    tz_utc = timezone(timedelta(hours=0))
    schedule = Scheduler(tzinfo=timezone.utc)
    schedule.daily(time(hour=0, minute=0, tzinfo=tz_utc), gatherer.gather_chat_members)
    while True:
        schedule.exec_jobs()
        sleep(1)
