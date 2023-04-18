from book.models import Book
from django.contrib import admin
from core.utils import mixins


@admin.register(Book)
class BookAdmin(mixins.AdminUserMixin):
    pass
