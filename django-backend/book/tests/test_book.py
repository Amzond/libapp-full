import datetime
import json
from unittest import mock

from author.models import Author
from book.models import Book
from core.tests import object_factory
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APITestCase


@mock.patch(
    'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2001,5,15,12))
)
class BookCrudTest(APITestCase):
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
        self.book = object_factory.create_book(
            title='Vakaru fronte nieko naujo',
            authors=[self.author.id]
        )
        
        self.book2 = object_factory.create_book(
            title='Rytu fronte nieko naujo',
            authors=[self.author2.id]
        )
        with open('book/tests/mockups/book_test_mockup.json', 'r') as mockups:
            self.expected_responses = json.load(mockups)
            
    def test_book_create(self):
        # GIVEN
        url = reverse('book-list')
        data = {
            'title': 'Karo menas',
            'authors': [self.author.id]
        }
        # WHEN
        response = self.client.post(url, data, format='json')
        response_json = response.json()
        response_json.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json, self.expected_responses['test_book_create'])
        
    def test_book_create_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('book-list')
        data = {
            'title': 'Karo menas',
            'authors': [self.author.id]
        }
        # WHEN
        response = self.client.post(url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        
    def test_book_list(self):
        # GIVEN
        url = reverse('book-list')
        # WHEN
        response = self.client.get(url)
        response_json = response.json()
        for book in response_json:
            book.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_book_list'])
        
    def test_book_list_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('book-list')
        # WHEN
        response = self.client.get(url)
        response_json = response.json()
        for book in response_json:
            book.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_book_list'])
        
    def test_book_partial_update(self):
        # GIVEN
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        data = {
            'title': 'Karo menas',
            'num_of_pages': 56,
            'release_year': 2023,
            'genre': 'Romanas',
            'status': '2',
            'rewards': 'Bestseller',
            'language': 'Lietuviu',
            'translator': 'Tomas Davidonis',
            'publisher': 'Alma Litera',
            'cover': 'Kietas'
        }
        # WHEN
        response = self.client.patch(url, data, format='json')
        response_json = response.json()
        response_json.pop('id', None)
        # THEN 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_book_partial_update'])
        
    def test_book_partial_update_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        data = {
            'title': 'Karo menas',
            'num_of_pages': 56,
            'release_year': 2023,
            'genre': 'Romanas',
            'status': '2',
            'rewards': 'Bestseller',
            'language': 'Lietuviu',
            'translator': 'Tomas Davidonis',
            'publisher': 'Alma Litera',
            'cover': 'Kietas'
        }
        # WHEN
        response = self.client.patch(url, data, format='json')
        response_json = response.json()
        response_json.pop('id', None)
        # THEN 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        
    def test_book_destroy(self):
        # GIVEN
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        # WHEN
        response = self.client.delete(url, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.all().count(), 1)
        
    def test_book_destroy_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        # WHEN
        response = self.client.delete(url, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        
    def test_book_create_existing(self):
        # GIVEN
        url = reverse('book-list')
        data = {
            'title': 'Vakaru fronte nieko naujo',
            'authors': [self.author.id]
        }
        # WHEN 
        response = self.client.post(url,data ,format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['title'][0], 'book with this title already exists.')
        
    def test_book_author_delete_async_no_books(self):
        # GIVEN
        self.assertEqual(Author.objects.all().count(), 2)
        self.assertEqual(Book.objects.all().count(), 2)
        url  = reverse('book-detail', kwargs={'pk': self.book.id})
        # WHEN
        response = self.client.delete(url, format='json')
        # THEN 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.all().count(), 1)
        self.assertEqual(Author.objects.all().count(), 1)