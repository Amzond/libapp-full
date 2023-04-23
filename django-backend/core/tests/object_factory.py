import random
import uuid

from author.models import Author
from book.models import Book
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()

def get_permisions(permission: str)-> Permission:
    
    app, model, permission =  permission.split(':', 2)
    
    return Permission.objects.get(
        content_type___app_label = f'{app}',
        content_type__model = f'{model}',
        codename=f'{permission}'
    )
    
def create_user(username: str, **params) -> User:
    
    salt = random.randint(1000,9999)
    
    first_name = params.get('first_name') or f'Vardenis{salt}'
    last_name = params.get('last_name') or f'Pavardenis{salt}'
    email = params.get('email') or f'{first_name}.{last_name}@library.lt'.lower()
    
    params.update(
        {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'username': username
        }
    )
    params.setdefault('date_joined', '2023-04-20T12:00:00.000Z')
    params.setdefault('is_active', True)
    params.setdefault('is_staff', False)
    params.setdefault('is_superuser', False)
    params.setdefault('password', 'testing')
    
    groups = params.pop('groups', []) or []
    user_permissions = params.pop('user_permissions', []) or []
    
    obj = User.objects.create(**params)
    obj.groups.set(groups)
    
    for permission in user_permissions:
        obj.permissions.add(get_permisions(permission=permission))
        
    return obj

def create_author(**params) -> Author:
    
    salt = random.randint(10000,99999)
    
    params.setdefault('id', uuid.uuid4())
    full_name = params.get('full_name') or f'Vardenis Pavardenis{salt}'
    
    email = params.get('email') or f'{full_name}@library.lt'.lower()
    
    
    params.setdefault('phone', '860000')
    params.setdefault('born', None)
    params.setdefault('country', None)
    params.setdefault('rewards', None)
    params.setdefault('number_of_books', None)
    
    params.update(
        {
            'full_name': full_name,
            'email': email
        }
    )
    obj = Author.objects.create(**params)
    
    return obj
  
  
def create_book(title: str, authors: list, **params):
    
    params.setdefault('id', uuid.uuid4())
    params.setdefault('num_of_pages', 55)
    params.setdefault('release_year', 2023)
    params.setdefault('genre', 'Detektyvas')
    params.setdefault('status', '0')
    params.setdefault('rewards', None)
    params.setdefault('isbn', None)
    params.setdefault('language', None)
    params.setdefault('translator', None)
    params.setdefault('publisher', None)
    params.setdefault('cover', None)
    
    params.update(
        {
            'title': title
        }
    )
    obj = Book.objects.create(**params)
    obj.authors.set(authors)
    return obj