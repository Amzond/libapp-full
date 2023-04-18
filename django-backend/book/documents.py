from author.models import Author
from book.models import Book
from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class BookDocument(Document):
    authors = fields.ObjectField(properties={
        'full_name': fields.TextField(),
        'email' : fields.TextField(),
        'phone' : fields.TextField()
    })
    class Index:
        name = settings.ELASTIC_BOOK_INDEX
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
            }

    class Django:
        model = Book 
        queryset_pagination = 100
        fields = [
            'title',
            'num_of_pages',
            'release_year',
            'status',
            'genre'
        ]
        related_models = [Author]
        
        
    def get_queryset(self):
        return super().get_queryset().prefetch_related('authors')
        
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Author):
            return related_instance.book_set.all()