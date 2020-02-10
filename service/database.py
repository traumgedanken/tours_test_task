"""Module to work with database"""
import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BaseClass, Tour


def _prepare_session(func):
    def wrapper(self, *args, **kwargs):
        self.session = self.session_maker()
        print('open')
        result = func(self, *args, **kwargs)
        self.session.close()
        print('close')
        return result

    return wrapper


dotenv.load_dotenv()


class Database:
    """Class to connect to database"""
    def __init__(self):
        db_url = os.getenv('DB_URL') or 'sqlite:///'
        self.engine = create_engine(db_url)
        BaseClass.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(self.engine)
        self.session = None

    @_prepare_session
    def get_all(self):
        return [tour.values_dict() for tour in self.session.query(Tour)]
