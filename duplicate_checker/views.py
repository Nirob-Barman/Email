# duplicate_checker/views.py
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm, FormatChoiceForm
from .models import DuplicateEmail


def check_duplicates(request):
    if request.method == 'POST':
        file_form = FileUploadForm(request.POST, request.FILES)
        format_form = FormatChoiceForm(request.POST)

        if file_form.is_valid() and format_form.is_valid():
            file = request.FILES['file']
            format = format_form.cleaned_data['format']

            try:
                if format == 'csv':
                    df = pd.read_csv(file)
                elif format == 'txt':
                    df = pd.read_csv(file, delimiter='\t')
                elif format == 'xlsx':
                    df = pd.read_excel(file)
                else:
                    return HttpResponse("Invalid file format")

                if 'email' not in df.columns:
                    available_columns = ', '.join(df.columns)
                    return HttpResponse(f"The 'email' column is not found in the file. "
                                        f"Available columns: {available_columns}")

                emails = df['email'].tolist()

                # Find duplicates in the file
                duplicate_emails_in_file = set(
                    [email for email in emails if emails.count(email) > 1])
                
                print(duplicate_emails_in_file)

                # Save unique emails to the database
                for email in set(emails):
                    # Check if the email already exists
                    if not DuplicateEmail.objects.filter(email=email).exists():
                        DuplicateEmail.objects.create(email=email)

                if duplicate_emails_in_file:
                    return render(request, 'duplicate_checker/result.html', {'duplicate_emails_in_file': duplicate_emails_in_file, 'emails': emails})
                else:
                    return render(request, 'duplicate_checker/result.html', {'no_duplicates': True, 'emails': emails})

            except pd.errors.EmptyDataError:
                return HttpResponse("The file is empty.")
            except pd.errors.ParserError:
                return HttpResponse("Error parsing the file. Please check the file format.")

    else:
        file_form = FileUploadForm()
        format_form = FormatChoiceForm()

    return render(request, 'duplicate_checker/check_duplicates.html', {'file_form': file_form, 'format_form': format_form})
