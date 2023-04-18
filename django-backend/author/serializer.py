from author.models import Author
from core.utils import mixins
from rest_framework import serializers


class AuthorSerializer(mixins.BaseSerializerMixin):
    
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = [
            'created_by', 
            'created_at', 
            'updated_by', 
            'updated_at'
            ]