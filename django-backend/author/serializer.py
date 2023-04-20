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
    def validate_born(self, value):
        if len(str(value)) > 4:
            raise serializers.ValidationError("Blogas metų formatas(MMMM)")
        return value