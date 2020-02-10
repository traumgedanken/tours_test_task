"""Module with tests for database"""
import unittest
import datetime
from service import Database

sample_tour = {
    'origin_country': 'xxx', 'destination_country': 'yyy',
    'duration_days': 777, 'start_date': datetime.date(2121, 12, 12)
}


class TestDatabase(unittest.TestCase):
    """Test cases for database module"""

    def setUp(self):
        """New database instance for every test cases"""
        self.database = Database('sqlite:///')

    def test_get_all_empty(self):
        """Get tours from empty database"""
        empty_list = list(self.database.get_all())
        self.assertEqual([], empty_list)

    def test_get_and_insert(self):
        """Test case for insert, get one and get all tours"""
        self.database.create(sample_tour)
        expected_tour = sample_tour.copy()
        expected_tour['tour_id'] = 1

        tour_from_db = self.database.get_one(1).values_dict()
        self.assertEqual(expected_tour, tour_from_db)

        tours_from_db = [tour.values_dict() for tour in self.database.get_all()]
        self.assertEqual([expected_tour], tours_from_db)

    def test_get_invalid_id(self):
        """Test case for getting tour by not existing id"""
        tour = self.database.get_one(42)
        self.assertIsNone(tour)

    def test_update(self):
        """Test case for updating tour"""
        self.database.create(sample_tour)
        new_values = {'destination_country': 'aaa', 'duration_days': 0}

        self.database.update(1, new_values)
        expected_tour = sample_tour.copy()
        expected_tour.update(new_values)
        expected_tour['tour_id'] = 1

        tour_from_db = self.database.get_one(1).values_dict()
        self.assertEqual(expected_tour, tour_from_db)

    def test_delete(self):
        """Test case for deleting tour"""
        self.database.create(sample_tour)

        self.assertIsNotNone(self.database.get_one(1))
        self.database.delete(1)
        self.assertIsNone(self.database.get_one(1))
