from book.models import Book
from core.utils import scrap
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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
def bookBook(request):
    if request.method =="POST":
        bookId = request.data.get('id')
        book = Book.objects.get(pk = bookId)
        book.status = 1
        book.save()
        return JsonResponse({'details': 'Knygos statusas pakeistas'})
    return JsonResponse({'details': ' Nepavyko'})

 

