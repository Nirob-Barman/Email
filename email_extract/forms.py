from django import forms


class EmailExtractorForm(forms.Form):
    text_input = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), max_length=100000)


class EmailValidationForm(forms.Form):
    email = forms.EmailField()


class BulkEmailListForm(forms.Form):
    name = forms.CharField(max_length=255)
    emails_file = forms.FileField(
        help_text='Upload a CSV file containing email addresses')

    def clean_emails_file(self):
        file = self.cleaned_data['emails_file']

        # Check if the file has a valid CSV extension
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Please upload a valid CSV file.')

        return file
