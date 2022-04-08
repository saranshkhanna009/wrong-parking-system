# Python Imports
import re

# Django Imports
from django.core.exceptions import ValidationError

# Third Party Django Imports

# Inter App Imports

# Local Imports

def name_validator(data):
    """
    validates name by matching to ^[a-zA-Z\s]+$ regex
    """

    if not re.match('^[a-zA-Z\.\s]+$', data):
        raise ValidationError('{0} is not a valid name'.format(data))
    return data

