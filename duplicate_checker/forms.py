from django import forms
from .models import DuplicateEmail


class FileUploadForm(forms.Form):
    file = forms.FileField()


class FormatChoiceForm(forms.Form):
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('txt', 'TXT'),
        ('xlsx', 'XLSX'),
    ]

    format = forms.ChoiceField(
        choices=FORMAT_CHOICES, widget=forms.RadioSelect)
