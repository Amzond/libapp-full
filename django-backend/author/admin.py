from author.models import Author
from core.utils import mixins
from django.contrib import admin


@admin.register(Author)
class AuthorAdmin(mixins.AdminUserMixin):
    pass