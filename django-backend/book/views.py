from author.tasks import task_author_delete
from book.models import Book
from book.serializer import BookSerializer
from core.utils import elastic, exceptions
from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class BookFilterSet(filters.FilterSet):
    full_text_search = filters.CharFilter(method='full_text_search_elastic', label='search')
    
    class Meta:
        model = Book
        fields = {
            'title': [
                'iexact', 
                'icontains'
                ],
            'num_of_pages': [
                'exact', 
                'gte', 
                'lte'
                ],
            'release_year': [
                'iexact', 
                'gte', 
                'lte'
                ],
            'genre': [
                'iexact', 
                'icontains'
                ],
            'authors__full_name': [
                'icontains', 
                'iexact'
                ]
        }
   
    def full_text_search_elastic(self, queryset, _,value):

        es = elastic.init_elastic()  
        payload = elastic.es_full_text_search_query(value)
        try:
            response = es.search(index=settings.ELASTIC_BOOK_INDEX, body=payload, _source=False)
            book_ids = [result['_id'] for result in response['hits']['hits']]
        except Exception:
            raise exceptions.ServiceUnavailable()
        results = queryset.filter(pk__in=book_ids)
        return results
    
# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     filterset_class = BookFilterSet
    
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         author_ids = list(instance.authors.values_list('pk', flat=True))
#         self.perform_destroy(instance)
#         task_author_delete.delay(author_ids)


class BookViewSet(viewsets.ViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = BookFilterSet
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset, 
            many=True,
            context={
                'request': request
                }
            )
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,            
            context={
                'request': request
                }
            )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            self.serializer_class(instance).data, 
            status=status.HTTP_201_CREATED
            )
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)
    
    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, 
            data=request.data,
            context={
                'request': request
                }
            )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class(instance).data)
    
    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, 
            data=request.data, 
            partial=True,
            context={
                'request': request
                }
            )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class(instance).data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        author_ids = list(instance.authors.values_list('pk', flat=True))
        instance.delete()
        task_author_delete.delay(author_ids)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = self.filterset_class(
            self.request.GET, 
            queryset=queryset).qs
        return queryset
