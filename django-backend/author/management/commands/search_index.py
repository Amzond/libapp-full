from django.core.paginator import Paginator
from django_elasticsearch_dsl.management.commands import search_index
from django_elasticsearch_dsl.registries import registry


class Command(search_index.Command):
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--chunk-size', type=int, help='define a chunk size',)
        parser.add_argument('--order-by-field', type=str, help='Define field to order by',)
        
    def _populate(self, models, options):
        parallel = options['parallel']
        order_by_field = options.get('order_by_field') or 'created_at'
        chunk_size = options.get('cunk_size') or 0
        
        assert isinstance(order_by_field, str) and order_by_field, 'Field name expected'
        assert isinstance(chunk_size, int) and chunk_size >= 0, 'Integer >= 0 expected'
        
        for doc in registry.get_documents(models):
            self.stdout.write("Indexing {} '{}' objects {}".format(
                doc.get_queryset().count() if options['count'] else "all",
                doc.django.model.__name__,
                "(parallel)" if parallel else ""
                )
            ) 
            chunk_size = chunk_size if chunk_size else getattr(doc.django, 'queryset_pagination', 25)
            
            paginator = Paginator(doc().get_queryset().order_by(order_by_field), chunk_size)
            
            for page_number in paginator.page_range:
                page = paginator.page(page_number)
                doc().update(page.object_list, parallel=parallel, refresh=options['refresh'])    
        