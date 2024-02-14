from django.contrib import admin
from .models import ExtractedEmail, ValidatedEmail, BulkEmailList

# Register your models here.
admin.site.register(ExtractedEmail)
admin.site.register(ValidatedEmail)
admin.site.register(BulkEmailList)
