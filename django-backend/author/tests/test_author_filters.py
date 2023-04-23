import datetime
import json
from unittest import mock
from urllib.parse import urlencode

from author.models import Author
from core.tests import object_factory
from django.urls import reverse
from django.utils.timezone import make_aware
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorFilterTests(APITestCase):
    FILTERS = {
        'test_born__gte': {
            'born__gte' : 2020
        },
        'test_born__lte': {
            'born__lte' : 2022
        }
    }

    @mock.patch(
        'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2000,5,15,12))
    )
    def setUp(self):
        self.user = object_factory.create_user(username='librarian')
        self.client.force_authenticate(user=self.user)
        self.author = object_factory.create_author(
            full_name = "Arturas Nes",
            email = "artnes@ktu.lt",
            born = '2019'
        )
        self.author2 = object_factory.create_author(
            full_name = "Tomas Dom",
            email = "tomdom@ktu.lt",
            born = '2023'
        )
        self.author3 = object_factory.create_author(
            full_name = "Dovis Tob",
            email = "dovtob@ktu.lt",
            born = '2021'
        )
        with open('author/tests/mockups/author_test_filters_mockup.json', 'r') as mockups:
            self.expected_responses = json.load(mockups)
    
    @parameterized.expand(
        [(name, filter_data) for name, filter_data in FILTERS.items()]
    )
    def test_author_filter(self, name, filter_data):
        # GIVEN 
        url = reverse('author-list')
        url = f'{url}?{urlencode(filter_data)}'
        # WHEN
        response = self.client.get(url,format='json')
        response_json = response.json()
        for author in response_json:
            author.pop('id', None)
        # THEN
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses[name])