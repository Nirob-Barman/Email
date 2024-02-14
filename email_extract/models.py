from django.db import models

# Create your models here.


class ExtractedEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class ValidatedEmail(models.Model):
    email = models.EmailField(unique=True)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class BulkEmailList(models.Model):
    name = models.CharField(max_length=255, unique=True)
    emails = models.ManyToManyField(
        ValidatedEmail, related_name='bulk_email_lists')

    def __str__(self):
        return self.name
