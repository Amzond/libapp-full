from author.serializer import AuthorSerializer
from book.models import Book
from core.utils import mixins


class BookSerializer(mixins.BaseSerializerMixin):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = [
            'created_by', 
            'created_at', 
            'updated_by', 
            'updated_at'
            ]