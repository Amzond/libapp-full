import datetime
import json
from io import StringIO
from unittest import mock
from unittest.mock import patch
from urllib.parse import urlencode

from author.documents import AuthorDocument
from author.models import Author
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
class AuthorSearchTests(APITestCase):
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
        with open('author/tests/mockups/author_test_mockup.json', 'r') as mockups:
            self.expected_responses = json.load(mockups)
            
    SEARCH_MOCK = json.load(
        open('author/tests/mockups/author_test_elastic_mockup.json')
    )

    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_author_elastic_search_full_name(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            return self.SEARCH_MOCK['test_author_search_elastic']
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'Arturas Nes'}
        
        url = reverse('author-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()
        for item in response_json:
            item.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_full_text_search'])
        mocked_es_search.assert_called_with(
            index='authors', body=self.SEARCH_MOCK['search_query'], _source=False
        )
        
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_author_elastic_search_full_name_two(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            return self.SEARCH_MOCK['test_author_search_elastic_two']
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'Arturas'}
        
        url = reverse('author-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()
        for item in response_json:
            item.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_full_text_search_two'])
        mocked_es_search.assert_called_with(
            index='authors', body=self.SEARCH_MOCK['search_query_two'], _source=False
        )
        
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_author_elastic_search_full_name_email(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            return self.SEARCH_MOCK['test_author_search_elastic_email']
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'artdom@ktu.lt'}
        
        url = reverse('author-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()
        for item in response_json:
            item.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_full_text_search_email'])
        mocked_es_search.assert_called_with(
            index='authors', body=self.SEARCH_MOCK['search_query_email'], _source=False
        )
    @mock.patch('elasticsearch.Elasticsearch.search')  
    def test_author_elastic_search_full_name_raise_error(self, mocked_es_search):
        # GIVEN
        def search_mock(*args, **kwargs):
            raise ConnectionTimeout()
        
        mocked_es_search.side_effect = search_mock
        
        search_query = {'full_text_search': 'artdom@ktu.lt'}
        
        url = reverse('author-list')
        url = f"{url}?{urlencode(search_query)}"
        # WHEN 
        response = self.client.get(url, format='json')
        response_json = response.json()

        # THEN
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response_json['detail'], 'Paslauga laikinai nepasiekiama' )
        
    def test_author_document(self):
        # GIVEN
        doc = AuthorDocument()
        author = object_factory.create_author(
            id= '1a27cc50-6cad-4ff9-aad5-c974eff014e4',
            full_name = 'Tadas Blinda',
            email='tadbli@ktu.lt',
            phone='860',
            born=2000,
            number_of_books = 5,
            country = 'Lietuva',
            rewards = 'Hero'
        )
        # WHEN
        with patch('django_elasticsearch_dsl.documents.bulk') as mock:
            doc.update(author)
            actions = [
                {
                    '_index': settings.ELASTIC_AUTHOR_INDEX,
                    '_op_type': 'index',
                    '_id': author.id,
                    '_source': {
                        'full_name': author.full_name,
                        'email': author.email,
                        'phone': author.phone,
                        'born': author.born,
                        'number_of_books': author.number_of_books,
                        'country': author.country,
                        'rewards': author.rewards
                    }
                }
            ]
        #THEN
        
            self.assertEqual(1, mock.call_count)
            self.assertEqual(actions, list(mock.call_args_list[0][1]['actions']))
            self.assertEqual(mock.call_args_list[0][1]['refresh'], True)
            self.assertEqual(doc._index.connection, mock.call_args_list[0][1]['client'])


class CallCommandsTestCase(TestCase):
    def test_populate_author(self):
        # GIVEN
        out = StringIO()
        args = ['--populate', '--model', 'author', '-f']
        # WHEN
        call_command('search_index', *args, stdout=out)
        # THEN
        self.assertEqual("Indexing 0 'Author' objects \n", out.getvalue())
        
    @mock.patch(
        'elasticsearch.Elasticsearch.bulk', mock.MagicMock(return_value={'items': []})
    )
    def test_populate_author_chunk(self):
        # GIVEN
        object_factory.create_author()
        object_factory.create_author()
        object_factory.create_author()
        out = StringIO()
        args = ['--populate', '--model', 'author', '-f', '--chunk-size', '2']
        # WHEN
        call_command('search_index', *args, stdout=out)
        # THEN
        self.assertEqual("Indexing 3 'Author' objects \n", out.getvalue())
        