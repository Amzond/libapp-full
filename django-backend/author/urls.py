from django.urls import path

from author.views import AuthorViewSet

urlpatterns = [
    path(
        '', 
        AuthorViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),  
        name='author-list'
    ),
    path(
        '<uuid:pk>', 
        AuthorViewSet.as_view({
            'get': 'retrieve', 
            'delete': 'destroy',
            'patch': 'partial_update'
        }), 
        name='author-detail'
    )
]