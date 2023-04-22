import json

from book.models import Book
from book.serializer import BookSerializer
from core.utils import scrap, utils
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import response
from rest_framework.decorators import api_view


@api_view(['POST'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def call_scrap(request):
    
    if request.method =="POST":
        book_store = request.data.get('book_store')
        url = request.data.get('url')
        if book_store == 'vaga':
            if url:
                added_books = scrap.scrap_books_from_vaga(url)
            else:
                added_books = scrap.scrap_books_from_vaga('')
            
            return JsonResponse({
                'details': 'Vaga done',
                'added_books': added_books
                })
        if book_store == 'knygos':
            if url:
                added_books = scrap.scrap_books_from_knygos(url)
            else:
                added_books = scrap.scrap_books_from_knygos('')
            return JsonResponse({
                'details': 'Knygos done',
                'added_books': added_books
                })
            

@api_view(['POST'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def call_scrap_single(request):
    
    if request.method =="POST":
        book_store = request.data.get('book_store')
        url = request.data.get('url')
        if book_store == 'vaga':
            if url:
                added_books = scrap.scrap_single_book_from_vaga(url)
    
                return JsonResponse({
                    'details': 'Vaga done',
                    'added_books': added_books
                    })
        if book_store == 'knygos':
            if url:
                added_books = scrap.scrap_single_book_from_knygos(url)
                return JsonResponse({
                    'details': 'Knygos done',
                    'added_books': added_books
                    })            

        
@api_view(['POST'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def bookBook(request):
    if request.method =="POST":
        bookId = request.data.get('id')
        book = Book.objects.get(pk = bookId)
        book.status = 1
        book.save()
        return JsonResponse({'details': 'Knygos statusas pakeistas'})
    return JsonResponse({'details': ' Nepavyko'})

@api_view(['GET'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def get_all_genres(request):
    if request.method =="GET":
        uniq_genres = utils.get_all_uniq_genres()
        return JsonResponse(list(uniq_genres), safe=False)
    return JsonResponse({'details': ' Nepavyko'})
 
@api_view(['GET'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def get_oldest_author_years(request):
    if request.method =="GET":
        oldest = utils.get_oldest_author()
        return JsonResponse(oldest, safe=False)
    return JsonResponse({'details': ' Nepavyko'})

@api_view(['GET'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def get_max_number_pages(request):
    if request.method =="GET":
        number = utils.get_max_num_of_pages()
        return JsonResponse(number, safe=False)
    return JsonResponse({'details': 'Nepavyko'})

@api_view(['GET'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def get_min_number_pages(request):
    if request.method =="GET":
        number = utils.get_min_num_of_pages()
        return JsonResponse(number, safe=False)
    return JsonResponse({'details': 'Nepavyko'})



@api_view(['POST'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def get_author_books(request):
    if request.method =="POST":
        author_uuid = request.data.get('uuid')
        books = utils.author_books(author_id=author_uuid)
        return JsonResponse(list(books), safe=False)
    return JsonResponse({'details': ' Nepavyko'})