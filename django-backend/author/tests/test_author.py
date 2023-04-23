import datetime
import json
from unittest import mock

from author.models import Author
from core.tests import object_factory
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APITestCase


@mock.patch(
    'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2001,5,15,12))
)
class AuthorCrudTests(APITestCase):
    @mock.patch(
        'django.utils.timezone.now', lambda: make_aware(datetime.datetime(2000,5,15,12))
    )
    def setUp(self):
        self.user = object_factory.create_user(username='librarian')
        self.client.force_authenticate(user=self.user)
        self.author = object_factory.create_author(
            full_name = "Arturas Nes",
            email = "artnes@ktu.lt",
        )
        self.author2 = object_factory.create_author(
            full_name = "Tomas Dom",
            email = "tomdom@ktu.lt",
        )
        with open('author/tests/mockups/author_test_mockup.json', 'r') as mockups:
            self.expected_responses = json.load(mockups)
        
    def test_author_create(self):

        # GIVEN
        url = reverse('author-list')
        data = {
            'full_name': 'Tomas Domauskas',
        }
        # WHEN
        response = self.client.post(url,data, format='json')
        response_json = response.json()
        response_json.pop('id', None)
        
        # THEN 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json, self.expected_responses['test_author_create'])
        
    def test_author_create_no_full_name(self):

        # GIVEN
        url = reverse('author-list')
        data = {
            'full_name': '',         
        }
        # WHEN
        response = self.client.post(url,data, format='json')
        # THEN 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['full_name'][0], 'This field may not be blank.')
        
    def test_author_create_no_auth(self):  
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('author-list')
        data = {
            'full_name': 'Tomas Domauskas',
        }
        # WHEN 
        response = self.client.post(url,data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        
    def test_author_list(self):
        # GIVEN
        url = reverse('author-list')
        # WHEN 
        response = self.client.get(url)
        response_json = response.json()
        for author in response_json:
            author.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_list'])
        
    def test_author_list_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('author-list')
        # WHEN 
        response = self.client.get(url)
        response_json = response.json()
        for author in response_json:
            author.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_list'])
        
    def test_author_partial_update(self):
        # GIVEN
        url = reverse(
            'author-detail',
            kwargs={'pk': self.author.id}
        )
        data ={
            'full_name': 'Hamlet'
        }
        # WHEN 
        response = self.client.patch(url, data, format='json')
        response_json = response.json()
        response_json.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_partial_update'])
    
    def test_author_partial_update_to_exist(self):
        # GIVEN
        url = reverse(
            'author-detail',
            kwargs={'pk': self.author.id}
        )
        data ={
            'full_name': 'Tomas Dom'
        }
        # WHEN 
        response = self.client.patch(url, data, format='json')

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['full_name'][0], 'author with this full name already exists.')
        
    def test_author_partial_update_data(self):
        # GIVEN
        url = reverse(
            'author-detail',
            kwargs={'pk': self.author.id}
        )
        data ={
            'email': 'newmail@ktu.lt',
            'born': 1999,
            'phone': '3700',
            'country': 'Lietuva',
            'rewards': 'Nera apdovanojimu',
            'number_of_books': 5
        }
        # WHEN 
        response = self.client.patch(url, data, format='json')
        response_json = response.json()
        response_json.pop('id', None)
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, self.expected_responses['test_author_partial_update_data'])
        
    def test_author_partial_update_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse(
            'author-detail',
            kwargs={'pk': self.author.id}
        )
        data ={
            'full_name': 'Hamlet'
        }
        # WHEN 
        response = self.client.patch(url, data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
    
    def test_author_destroy_assigned_to_book(self):
        # GIVEN
        book = object_factory.create_book(
            title="Vakaru fronte nieko naujo",
            authors=[self.author.id]
        )
        self.author.book_set.add(book)
        url = reverse('author-detail', kwargs={'pk': self.author.id})
        # WHEN 
        response = self.client.delete(url, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], 'Negalima ištrinti autoriaus, nes jis turi knygų')
        
    def test_author_destroy(self):
        # GIVEN
        url = reverse('author-detail', kwargs={'pk': self.author.id})
        # WHEN 
        response = self.client.delete(url, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual( Author.objects.all().count(), 1)
        
    def test_author_destroy_no_auth(self):
        # GIVEN
        self.client.force_authenticate(user=None)
        url = reverse('author-detail', kwargs={'pk': self.author.id})
        # WHEN 
        response = self.client.delete(url, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        self.assertEqual( Author.objects.all().count(), 2)    
