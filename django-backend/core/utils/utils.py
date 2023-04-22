import json

from author.models import Author
from book.models import Book
from django.core import serializers
from django.db.models import Max, Min
from django.shortcuts import get_object_or_404


def get_all_uniq_genres():
    
    return Book.objects.exclude(genre=None).values_list('genre', flat=True).distinct()


def get_oldest_author():
    oldest_author = Author.objects.filter(born__isnull=False).annotate(min_born=Min('born')).order_by('min_born').first()
    return oldest_author.born

def get_max_num_of_pages():
    bigest_number_of_pages = Book.objects.filter(num_of_pages__isnull=False).annotate(max_number=Max('num_of_pages')).order_by('-max_number').first()

    return bigest_number_of_pages.num_of_pages

def get_min_num_of_pages():
    smallest_number_of_pages = Book.objects.filter(num_of_pages__isnull=False).annotate(min_number=Min('num_of_pages')).order_by('min_number').first()
    
    return smallest_number_of_pages.num_of_pages

def author_books(author_id):
    queryset = get_object_or_404(Author, pk=author_id)
    books = queryset.book_set.all().values('id','title', 'num_of_pages', 'genre', 'release_year')
    return books