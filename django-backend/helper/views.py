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
        url = request.data.get('book_url')
        if book_store == 'vaga':
            if url:
                scrap.scrap_books_from_vaga(url)
            else:
                scrap.scrap_books_from_vaga('')
            
            return JsonResponse({'details': 'Vaga done'})
        if book_store == 'knygos':
            if url:
                scrap.scrap_books_from_knygos(url)
            else:
                scrap.scrap_books_from_knygos('')
            return JsonResponse({'details': 'Knygos done'})

        
@api_view(['POST'])
@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def bookBook(request):
    if request.method =="POST":
        bookId = request.data.get('id')
        book = Book.objects.get(pk = bookId)
        book.status = 1
        book.save()
        return JsonResponse({'details': 'Status changed'})
    return JsonResponse({'details': ' Failed'})

 

