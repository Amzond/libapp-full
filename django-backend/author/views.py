from author.models import Author
from author.serializer import AuthorSerializer
from core.utils import elastic, exceptions
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class AuthorFilterSet(filters.FilterSet):
    full_text_search = filters.CharFilter(method='full_text_search_elastic', label='search')
    
    class Meta:
        model = Author
        fields = {
            'full_name': [
                'iexact', 
                'icontains'
                ],
            'email': [
                'iexact', 
                'icontains'
                ],
            'phone': [
                'iexact', 
                'icontains'
                ] ,
            'born':[
                'gte',
                'lte'
                ]
        }

    def full_text_search_elastic(self, queryset, _,value):

        es = elastic.init_elastic()  
        payload = elastic.es_full_text_search_query(value)
        try:
            response = es.search(index=settings.ELASTIC_AUTHOR_INDEX, body=payload, _source=False)
            author_ids = [result['_id'] for result in response['hits']['hits']]
            # hits = response['hits']['hits']
            # author_ids = []
            # for hit in hits:
            #     author_id = hit['_id']
            #     author_ids.append(author_id)
        except Exception:
            raise exceptions.ServiceUnavailable()
        return queryset.filter(pk__in=author_ids)

            
class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = AuthorFilterSet
    

    def list(self, request):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(
            queryset, 
            many=True, 
            context={
                'request': request
                }
            )
        return super().list(self,request)

    def create(self, request):
        serializer = AuthorSerializer(
            data=request.data,  
            context={
                'request': request
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(
            queryset, 
            data=request.data,  
            context={
                'request': request
                }
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(
            queryset, 
            data=request.data, 
            partial=True,  
            context={
                'request': request
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Author, pk=pk)
        if queryset.book_set.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'Negalima ištrinti autoriaus, nes jis turi knygų'}
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    