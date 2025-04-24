from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    # Regex to match international phone numbers
    phone_regex = r'^\+?\d{9,15}$'
    if not re.match(phone_regex, value):
        raise ValidationError(
            'Invalid phone number. Please enter a valid phone number.')
