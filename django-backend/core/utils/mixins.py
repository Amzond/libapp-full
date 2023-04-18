import uuid
from collections import OrderedDict

from django.conf import settings
from django.contrib import admin
from django.db import models
from rest_framework import serializers


class BaseSerializerMixin(serializers.ModelSerializer):
    
    def validate(self, validated_data: OrderedDict) -> OrderedDict:
        if not self.instance:
            validated_data.update({
                'created_by': self.context['request'].user
            })
        validated_data.update({
            'updated_by': self.context['request'].user
        })
        
        return validated_data


class AdminUserMixin(admin.ModelAdmin):
    
    readonly_fields = [
        'created_at',
        'created_by',
        'updated_at',
        'updated_by'
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        
        return super().save_model(request, obj, form, change)

class UUIDPrimaryKeyMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False
    )
    
    class Meta:
        abstract = True
     
     
        
class DefaultValuesMixin(models.Model):
     
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_created_by',
        on_delete=models.SET_NULL, null=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_updated_by',
        on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
    
