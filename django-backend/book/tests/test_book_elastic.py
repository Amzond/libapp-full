import datetime
import json
from io import StringIO
from unittest import mock
from unittest.mock import patch
from urllib.parse import urlencode

from book.documents import BookDocument
from book.models import Book
from core.tests import object_factory
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware
from elasticsearch.exceptions import ConnectionTimeout
from rest_framework import status
from rest_framework.test import APITestCase


@mock.patch(
    'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2001,5,15,12))
)
class BookSearchTests(APITestCase):
    @mock.patch(
        'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2000,5,15,12))
    )
    def setUp(self):
        self.user = object_factory.create_user(username='librarian')
        self.client.force_authenticate(user=self.user)
        self.author = object_factory.create_author(
            id = '1a27cc50-6cad-4ff9-aad5-c974eff014e1',
            full_name = 'Arturas Nes',
            email = 'artnes@ktu.lt',
        )
        self.author2 = object_factory.create_author(
            id = '1a27cc50-6cad-4ff9-aad5-c974eff014e2',
            full_name = 'Tomas Dom',
            email = 'tomdom@ktu.lt',
        )
        self.author3 = object_factory.create_author(
            id = '1a27cc50-6cad-4ff9-aad5-c974eff014e3',
            full_name = 'Arturas Dom',
            email = 'artdom@ktu.lt',
        )
        self.book = object_factory.create_book(
            id= '7804d3a7-616a-4300-84db-1df153a023f1',
            title='Vakaru fronte nieko naujo',
            authors=[self.author.id]
        )
        
        self.book2 = object_factory.create_book(
            id= '7804d3a7-616a-4300-84db-1df153a023f2',
            title='Rytu fronte nieko naujo',
            authors=[self.author2.id]

        )
        
        with open('book/tests/mockups/book_test_mockup.json', 'r') as mockups:
            self.expected_responses = json.load(mockups)
            
    SEARCH_MOCK = json.load(
        open('book/tests/mockups/book_test_elastic.json')
    )
    
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_book_elastic_search_title(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            return self.SEARCH_MOCK['test_book_search_elastic']
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'Vakaru'}
        
        url = reverse('book-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()
        for item in response_json:
            item.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_book_full_text_search'])
        mocked_es_search.assert_called_with(
            index='books', body=self.SEARCH_MOCK['search_query'], _source=False
        )
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_book_elastic_search_title_two(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            return self.SEARCH_MOCK['test_book_search_elastic_two']
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'fronte'}
        
        url = reverse('book-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()
        for item in response_json:
            item.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_book_full_text_search_two'])
        mocked_es_search.assert_called_with(
            index='books', body=self.SEARCH_MOCK['search_query_two'], _source=False
        )
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_book_elastic_search_full_name_raise_error(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            raise ConnectionTimeout()
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'fronte'}
        
        url = reverse('book-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()

        # THEN
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response_json['detail'], 'Paslauga laikinai nepasiekiama' )
        
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_book_elastic_search_genre(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            return self.SEARCH_MOCK['test_book_search_elastic_two']
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'Detektyvas'}
        
        url = reverse('book-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()
        for item in response_json:
            item.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_book_full_text_search_two'])
        mocked_es_search.assert_called_with(
            index='books', body=self.SEARCH_MOCK['search_query_genre'], _source=False
        )
    
    def test_book_document(self):
        # GIVEN
        doc = BookDocument()
        # WHEN
        with patch('django_elasticsearch_dsl.documents.bulk') as mock:
            doc.update(self.book)
            actions = [
                {
                    '_op_type': 'index',
                    '_index': settings.ELASTIC_BOOK_INDEX,
                    '_id': self.book.id,
                    '_source': {
                        'authors': [{
                            'full_name': self.author.full_name,
                            'email': self.author.email,
                            'phone': self.author.phone,
                        }],
                        'title': self.book.title,
                        'num_of_pages': self.book.num_of_pages,
                        'release_year': self.book.release_year,
                        'status': self.book.status,
                        'genre': self.book.genre,
                        'isbn': self.book.isbn,
                        'rewards': self.book.isbn,
                        'language': self.book.language,
                        'translator': self.book.translator,
                        'publisher': self.book.publisher,
                        'cover': self.book.cover
                    }
                }
            ]
            #THEN
            self.assertEqual(1, mock.call_count)
            self.assertEqual(actions, list(mock.call_args_list[0][1]['actions']))
            self.assertEqual(mock.call_args_list[0][1]['refresh'], True)
            self.assertEqual(doc._index.connection, mock.call_args_list[0][1]['client'])