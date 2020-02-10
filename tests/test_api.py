"""Module with tests for database"""
import unittest

from flask_api import status

from rest import app
from service import Database

sample_tour = {
    'origin_country': 'xxx', 'destination_country': 'yyy',
    'duration_days': 777, 'start_date': '2121-12-12'
}


class TestDatabase(unittest.TestCase):
    """Test cases for database module"""

    def setUp(self):
        config = app.app.config
        config['TESTING'] = True
        config['WTF_CSRF_ENABLED'] = False
        config['DEBUG'] = False
        config['DATABASE'] = Database('sqlite:///')

        self.app = app.app.test_client()

    def test_get_empty_list(self):
        """Test case for getting empty list of tours"""
        response = self.app.get('/api/tour')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.json)

    def test_get_invalid_id(self):
        """Test case for getting tour by invalid id"""
        response = self.app.get('/api/tour/42')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_and_insert(self):
        """Test case for insert, get one and get all tours"""
        response = self.app.post('/api/tour', json=sample_tour)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        expected_tour = sample_tour.copy()
        expected_tour['tour_id'] = 1
        response = self.app.get('/api/tour/1')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_tour, response.json)

        response = self.app.get('/api/tour')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([expected_tour], response.json)

    def test_update_valid_info(self):
        """Test for update a tour with valid data"""
        self.app.post('/api/tour', json=sample_tour)
        new_values = {'destination_country': 'aaa', 'duration_days': 0}
        response = self.app.put('/api/tour/1', json=new_values)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected_tour = sample_tour.copy()
        expected_tour.update(new_values)
        expected_tour['tour_id'] = 1
        response = self.app.get('/api/tour/1')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_invalid_invalid_info(self):
        """Test for updating with invalid values"""
        self.app.post('/api/tour', json=sample_tour)

        response = self.app.put('/api/tour/1', json={'destination_country': 0})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.app.put('/api/tour/1', json={'origin_country': 0})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.app.put('/api/tour/1', json={'duration_days': 'string'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.app.put('/api/tour/1', json={'start_date': '1/11/2012'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_ivalid_index(self):
        """Test case for updating with invalid index"""
        response = self.app.put('/api/tour/1', json={'duration_days': 15})
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_invalid_index(self):
        """Test case for deleting with invalid index"""
        response = self.app.delete('/api/tour/1')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_valid_index(self):
        """Test case for deleting with valid index"""
        self.app.post('/api/tour', json=sample_tour)
        response = self.app.delete('/api/tour/1')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
