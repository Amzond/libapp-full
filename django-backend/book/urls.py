from book.views import BookViewSet
from django.urls import path

urlpatterns = [
    path(
        '', 
        BookViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),  
        name='book-list'
    ),
    path(
        '<uuid:pk>', 
        BookViewSet.as_view({'get': 'retrieve', 
                             'delete': 'destroy',
                             'patch': 'partial_update'}), 
        name='book-detail'
    )
]