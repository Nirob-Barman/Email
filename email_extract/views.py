from django.shortcuts import render
from .forms import EmailExtractorForm
import re
from .models import ExtractedEmail, ValidatedEmail, BulkEmailList
from .forms import EmailValidationForm, BulkEmailListForm
import requests
from django.http import HttpResponse


def extract_emails(text):
    # Use a regular expression to extract email addresses from the input text
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)


def email_extractor(request):
    if request.method == 'POST':
        form = EmailExtractorForm(request.POST)
        if form.is_valid():
            text_input = form.cleaned_data['text_input']
            emails = extract_emails(text_input)

            # Save emails to the database
            for email in emails:
                # Check if the email already exists in the database
                if not ExtractedEmail.objects.filter(email=email).exists():
                    # If it doesn't exist, create a new record
                    ExtractedEmail.objects.create(email=email)

            return render(request, 'email_extract/result.html', {'emails': emails})

    else:
        form = EmailExtractorForm()

    return render(request, 'email_extract/email_extractor.html', {'form': form})


def validate_email(email):
    # Make API request to validate email
    api_url = f"https://api.ValidEmail.net/?email={email}&token=605040dd66604f58a5f3d6d7677bf166"
    response = requests.get(api_url)
    # Print the entire API response
    # print(response.text)

    # Check if the email is valid based on the API response
    is_valid = response.json().get('IsValid', False)
    # print(is_valid)
    return is_valid


def validate_email_view(request):
    if request.method == 'POST':
        form = EmailValidationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Validate the email using the API
            is_valid = validate_email(email)

            # Validate the email using the API
            is_valid = validate_email(email)

            # Check if a record with the email already exists
            existing_record = ValidatedEmail.objects.filter(
                email=email).first()

            if existing_record:
                # Update the existing record
                existing_record.is_valid = is_valid
                existing_record.save()
            else:
                # Create a new record if it doesn't exist
                ValidatedEmail.objects.create(email=email, is_valid=is_valid)

            return render(request, 'email_extract/validation_result.html', {'email': email, 'is_valid': is_valid})
    else:
        form = EmailValidationForm()

    return render(request, 'email_extract/validate_email.html', {'form': form})


# def validate_bulk_email_list(request):
#     if request.method == 'POST':
#         # Assuming you have a form to upload a CSV file containing email addresses
#         # You need to implement this form in forms.py and handle the file upload
#         # For simplicity, let's assume the form is named BulkEmailListForm
#         bulk_email_list_form = BulkEmailListForm(request.POST, request.FILES)

#         if bulk_email_list_form.is_valid():
#             name = bulk_email_list_form.cleaned_data['name']
#             emails_file = bulk_email_list_form.cleaned_data['emails_file']

#             # Process the CSV file and validate each email
#             # email_list = [line.strip() for line in emails_file]
#             email_list = [line.decode('utf-8').strip() for line in emails_file]
#             print(email_list)

#             # Create a new bulk email list
#             bulk_email_list, created = BulkEmailList.objects.get_or_create(name=name)
            
#             # Validate and save each email in the bulk email list
#             email_list_with_status = []  # To store pairs of email and validation status

#             # Validate and save each email in the bulk email list
#             for email in email_list:
#                 # print('email', email)
#                 email_str = email.decode('utf-8') if isinstance(email, bytes) else email

#                 validated_email, created = ValidatedEmail.objects.get_or_create(email=email_str, is_valid=False)
#                 bulk_email_list.emails.add(validated_email)

#                 print("Validated email list", email_str)

#                 # Validate the email after creating the ValidatedEmail object
#                 is_valid = validate_email(email_str)
#                 validated_email.is_valid = is_valid
#                 validated_email.save()
            
#             # Pair each email with its validation status
#             # email_list_with_status = [(email_str, is_valid) for email_str in email_list]
#             email_list_with_status.append((email_str, is_valid))
#             print(email_list_with_status)
#             # return HttpResponse(f"Bulk Email List '{name}' has been processed.")
#             return render(request, 'email_extract/bulk_email_list_result.html', {'name': name, 'email_list': email_list_with_status})

#     else:
#         bulk_email_list_form = BulkEmailListForm()

#     return render(request, 'email_extract/validate_bulk_email_list.html', {'form': bulk_email_list_form})


# def validate_bulk_email_list(request):
#     if request.method == 'POST':
#         bulk_email_list_form = BulkEmailListForm(request.POST, request.FILES)

#         if bulk_email_list_form.is_valid():
#             name = bulk_email_list_form.cleaned_data['name']
#             emails_file = bulk_email_list_form.cleaned_data['emails_file']

#             email_list_with_status = []

#             # Create a new bulk email list
#             bulk_email_list, created = BulkEmailList.objects.get_or_create(
#                 name=name)

#             for email in emails_file:
#                 email_str = email.decode(
#                     'utf-8').strip() if isinstance(email, bytes) else email.strip()

#                 # Validate the email after creating the ValidatedEmail object
#                 is_valid = validate_email(email_str)

#                 validated_email, created = ValidatedEmail.objects.get_or_create(
#                     email=email_str, is_valid=is_valid)
#                 bulk_email_list.emails.add(validated_email)

#                 # Pair each email with its validation status
#                 email_list_with_status.append(
#                     {'email': email_str, 'is_valid': is_valid})
#                 print("List: ", email_list_with_status)

#             return render(request, 'email_extract/bulk_email_list_result.html', {'name': name, 'email_list': email_list_with_status})

#     else:
#         bulk_email_list_form = BulkEmailListForm()

#     return render(request, 'email_extract/validate_bulk_email_list.html', {'form': bulk_email_list_form})


def validate_bulk_email_list(request):
    if request.method == 'POST':
        bulk_email_list_form = BulkEmailListForm(request.POST, request.FILES)

        if bulk_email_list_form.is_valid():
            name = bulk_email_list_form.cleaned_data['name']
            emails_file = bulk_email_list_form.cleaned_data['emails_file']

            email_list_with_status = []

            # Create a new bulk email list
            bulk_email_list, created = BulkEmailList.objects.get_or_create(
                name=name)

            for email in emails_file:
                email_str = email.decode(
                    'utf-8').strip() if isinstance(email, bytes) else email.strip()

                # Check if ValidatedEmail with the given email already exists
                validated_email = ValidatedEmail.objects.filter(
                    email=email_str).first()

                if validated_email:
                    # If it exists, update the existing record
                    is_valid = validate_email(email_str)
                    validated_email.is_valid = is_valid
                    validated_email.save()
                else:
                    # If it doesn't exist, create a new ValidatedEmail object
                    is_valid = validate_email(email_str)
                    validated_email = ValidatedEmail.objects.create(
                        email=email_str, is_valid=is_valid)

                # Associate ValidatedEmail with the BulkEmailList
                bulk_email_list.emails.add(validated_email)

                # Pair each email with its validation status
                email_list_with_status.append(
                    {'email': email_str, 'is_valid': is_valid})

                print("List: ", email_list_with_status)

            return render(request, 'email_extract/bulk_email_list_result.html', {'name': name, 'email_list': email_list_with_status})

    else:
        bulk_email_list_form = BulkEmailListForm()

    return render(request, 'email_extract/validate_bulk_email_list.html', {'form': bulk_email_list_form})
