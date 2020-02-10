"""Module to work with database"""
import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BaseClass, Tour


def _prepare_session(func):
    def wrapper(self, *args, **kwargs):
        self.session = self.session_maker()
        result = func(self, *args, **kwargs)
        self.session.close()
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
        """
        This function is used to get list of all tours
        :return: list of tour objects
        """
        return self.session.query(Tour)

    @_prepare_session
    def get_one(self, tour_id):
        """
        This function is used to get only one tour object
        :param tour_id: ID of tour
        :return: tour object by given ID
        """
        return self.session.query(Tour).get(tour_id)

    @_prepare_session
    def create(self, tour):
        """
        This function creates new tour object and adds it to DB
        :param tour: dictionary with tour's info
        """
        new_tour = Tour(**tour)
        self.session.add(new_tour)
        self.session.commit()

    @_prepare_session
    def update(self, tour_id, tour_upd):
        """
        This function updates tour in DB
        :param tour_id: ID of tour to be updated
        :param tour_upd: new tour's info
        :return: True if found, False if not found
        """
        tour = self.session.query(Tour).get(tour_id)
        if not tour:
            return False

        for prop, value in tour_upd.items():
            setattr(tour, prop, value)
        self.session.commit()
        return True

    @_prepare_session
    def delete(self, tour_id):
        """
        This function deletes tour in DB
        :param tour_id: ID of tour to be deleted
        :return: True if found, False if not found
        """
        tour = self.session.query(Tour).get(tour_id)
        if not tour:
            return False

        self.session.delete(tour)
        self.session.commit()
        return True
