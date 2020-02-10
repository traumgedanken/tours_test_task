"""Module to implement CRUD operations"""
import datetime
import re

from flask_api import status
from sqlalchemy import exc

from rest.app import app


def _db_instance():
    return app.app.config['DATABASE']


def _process_date_property(tour):
    if 'start_date' not in tour:
        return

    date_str = tour.get('start_date')
    date_regexp = re.compile('([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')
    if not date_regexp.match(date_str):
        raise ValueError('Invalid data string')

    year, day, month = [int(n) for n in date_str.split('-')]
    tour['start_date'] = datetime.date(year, month, day)


def _bad_date_parameter_response(tour):
    return {
        "detail": f"'{tour['start_date']}' is not of type 'date' - 'yyyy-dd-mm'",
        "status": status.HTTP_400_BAD_REQUEST
    }, status.HTTP_400_BAD_REQUEST


def get_all():
    """
    This function responds to a request for /api/tour
    with the complete lists of tours
    :return: list of JSON serializable tour objects
    """
    return [tour.values_dict() for tour in _db_instance().get_all()]


def get_one(tour_id):
    """
    This function responds to a request for /api/tour/{tour_id}
    with one matching tour from tours
    :param tour_id: unique ID of tour to be found
    :return: tour matching ID
    """
    tour = _db_instance().get_one(tour_id)
    if tour:
        return tour.values_dict()
    return {'status': status.HTTP_404_NOT_FOUND}, status.HTTP_404_NOT_FOUND


def create(tour):
    """
    This function creates a new tour in the tour list
    based on the passed in tour data
    :param tour: tour to create in tours list
    :return: 201 on success, 406 on bad request
    """
    try:
        _process_date_property(tour)
        _db_instance().create(tour)
        return {'status': status.HTTP_201_CREATED}, status.HTTP_201_CREATED
    except exc.DataError:
        return _bad_date_parameter_response(tour)
    except (TypeError, ValueError):
        return {
            "detail": f"Missing one of mandatory property",
            "status": status.HTTP_400_BAD_REQUEST
        }, status.HTTP_400_BAD_REQUEST


def update(tour_id, tour_upd):
    """
    This function updates an existing tour in the tours list
    :param tour_id: ID of tour to update in the tours list
    :param tour_upd: tour info to update
    :return: 200 if updated, 404 if not found
    """
    try:
        _process_date_property(tour_upd)
        found = _db_instance().update(tour_id, tour_upd)
        if found:
            return {'status': status.HTTP_200_OK}, status.HTTP_200_OK
        return {'status': status.HTTP_404_NOT_FOUND}, status.HTTP_404_NOT_FOUND
    except (exc.DataError, ValueError):
        return _bad_date_parameter_response(tour_upd)


def delete(tour_id):
    """
    This function deletes a tour from the tours list
    :param tour_id: id of tour to be deleted
    :return: 200 if deleted, 404 if not found
    """
    found = _db_instance().delete(tour_id)
    if found:
        return {'status': status.HTTP_200_OK}, status.HTTP_200_OK
    return {'status': status.HTTP_404_NOT_FOUND}, status.HTTP_404_NOT_FOUND
