from django.urls import path
from .views import check_duplicates

urlpatterns = [
    path('check_duplicates/', check_duplicates, name='check_duplicates'),
]
