from django.urls import path
from . import views

urlpatterns = [
    path('email_extractor/', views.email_extractor, name='email_extractor'),
    path('validate_email/', views.validate_email_view, name='validate_email'),
    path('validate-bulk-email-list/', views.validate_bulk_email_list,
         name='validate_bulk_email_list'),
]