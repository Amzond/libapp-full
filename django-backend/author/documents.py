from author.models import Author
from django.conf import settings
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class AuthorDocument(Document):
    class Index:
        name = settings.ELASTIC_AUTHOR_INDEX
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
            }

    class Django:
        model = Author 
        queryset_pagination = 100
        fields = [
            'full_name',
            'email',
            'phone',
            
        ]
        