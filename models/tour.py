"""Module with ORM class definition"""
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

BaseClass = declarative_base()


class Tour(BaseClass):
    """Tour class to work with DB using ORM"""
    __tablename__ = 'tour'

    tour_id = Column(Integer, primary_key=True)
    origin_country = Column(String, nullable=False)
    destination_country = Column(String, nullable=False)
    duration_days = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)

    def __init__(self, origin_country, destination_country, duration_days, start_date):
        self.origin_country = origin_country
        self.destination_country = destination_country
        self.duration_days = duration_days
        self.start_date = start_date

    def values_dict(self):
        """This function return JSON serializable copy of tour object"""
        return {
            'tour_id': self.tour_id,
            'origin_country': self.origin_country,
            'destination_country': self.destination_country,
            'duration_days': self.duration_days,
            'start_date': self.start_date,
        }
