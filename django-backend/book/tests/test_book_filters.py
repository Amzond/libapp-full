import datetime
import json
from unittest import mock
from urllib.parse import urlencode

from book.models import Book
from core.tests import object_factory
from django.urls import reverse
from django.utils.timezone import make_aware
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


class BookFilterTests(APITestCase):
    
    FILTERS = {
        'test_num_of_pages_gte': {
            'num_of_pages__gte': 50
        },
        'test_num_of_pages__lte': {
            'num_of_pages__lte' : 56
        },
        'test_release_year__gte':{
            'release_year__gte': 2020
        },
        'test_release_year__lte':{
            'release_year__lte': 2022
        },
        'test_genre__iexact':{
            'genre__iexact': 'Detektyvas'
        },
        'test_status__exact':{
            'status': '1'
        }
    }

    @mock.patch(
        'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2000,5,15,12))
    )
    def setUp(self):
        self.user = object_factory.create_user(username='librarian')
        self.client.force_authenticate(user=self.user)
        self.author = object_factory.create_author(
            id = '1a27cc50-6cad-4ff9-aad5-c974eff014e1',
            full_name = "Arturas Nes",
            email = "artnes@ktu.lt",
            born = '2019'
        )
        self.author2 = object_factory.create_author(
            id = '1a27cc50-6cad-4ff9-aad5-c974eff014e2',
            full_name = "Tomas Dom",
            email = "tomdom@ktu.lt",
            born = '2023'
        )
        self.book = object_factory.create_book(
            title='Vakaru fronte nieko naujo',
            authors=[self.author.id],
            num_of_pages = 58,
            release_year = 2019
        )
        
        self.book2 = object_factory.create_book(
            title='Rytu fronte nieko naujo',
            authors=[self.author2.id],
            num_of_pages = 49,
            release_year = 2023,
            status = '1'
        )

        with open('book/tests/mockups/book_test_filter_mockup.json', 'r') as mockups:
            self.expected_responses = json.load(mockups)
        
    
    @parameterized.expand([(name, filter_data) for name, filter_data in FILTERS.items()]
    )
    def test_book_filter(self, name, filter_data):
        # GIVEN

        url = reverse('book-list')

        url = f'{url}?{urlencode(filter_data)}'
        # WHEN

        response = self.client.get(url, format='json')
        response_json = response.json()
        for book in response_json:
            book.pop('id', None)
        # THEN
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses[name])        