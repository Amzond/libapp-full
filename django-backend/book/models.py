import datetime

from author.models import Author
from core.utils import mixins
from django.db import models

BOOK_STATUS_CODES = (
    ('0', 'Nėra'),
    ('1', 'Užsakyta'),
    ('2', 'Yra'),
)


class Book(
    mixins.UUIDPrimaryKeyMixin,
    mixins.DefaultValuesMixin
):
    title = models.CharField(
        max_length=254, 
        unique=True
        )
    num_of_pages = models.PositiveIntegerField(
        default=0, 
        null=True, 
        blank=True
        )
    release_year = models.PositiveIntegerField(
        default=datetime.datetime.now().year, 
        null=True, 
        blank=True
        )
    authors = models.ManyToManyField(to=Author)
    genre = models.CharField(
        max_length=254, 
        blank=True, 
        null=True
        )
    status = models.CharField(
        max_length = 1, 
        choices = BOOK_STATUS_CODES, 
        default = 0
        )
    rewards = models.CharField(
        max_length= 100,
        blank=True,
        null=True
        )
    isbn = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    translator = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    publisher = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    cover = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    
    
    def __str__(self):
        return f'{self.title}'
