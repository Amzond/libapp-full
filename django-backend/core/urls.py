"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from helper import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authors/', include('author.urls')),
    path('api/books/', include('book.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair' ),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/scrape/', views.call_scrap, name='scrape_data'),
    path('api/change-status/', views.bookBook, name='change_book_status'),
    path('api/get-all-genres/', views.get_all_genres, name='getAllGenres' ),
    path('api/get-oldest-author-years/', views.get_oldest_author_years, name='get-oldest-author'),
    path('api/get-author-books/', views.get_author_books, name='get-author-books' ),
    path('api/scrap-single-book/', views.call_scrap_single, name='scrap-single-book'),
    path('api/get-max-pages/', views.get_max_number_pages, name='get-max-number'),
    path('api/get-min-pages/', views.get_min_number_pages, name='get-min-pages')
]
