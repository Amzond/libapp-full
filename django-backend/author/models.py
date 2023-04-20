from core.utils import mixins
from django.db import models


class Author(
    mixins.UUIDPrimaryKeyMixin,
    mixins.DefaultValuesMixin
):
    full_name = models.CharField(
        max_length=100, 
        unique=True
    )
    email = models.EmailField(
        max_length=50,
        blank=True, 
        null=True
    )
    phone = models.CharField(
        max_length=16, 
        blank=True, 
        null=True
    )
    born = models.PositiveIntegerField(
        null=True, 
        blank=True
        )
    country = models.CharField(
        blank = True,
        null = True,
        max_length=50
    )
    rewards = models.CharField(
        blank = True,
        null = True,
        max_length=50
    )
    number_of_books = models.PositiveIntegerField(
        blank = True,
        null = True,
    )
    
    
    def __str__(self):
        return f'{self.full_name}'


    