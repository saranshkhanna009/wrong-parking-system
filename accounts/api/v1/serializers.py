
# django imports
from django.contrib.auth import get_user_model

# third party imports
from rest_framework import serializers
from phonenumber_field.validators import validate_international_phonenumber

User = get_user_model()


class SendOTPSerializer(serializers.Serializer):
    """
    Send Otp to requested Mobile Number
    """
    mobile_number = serializers.CharField(
        validators=[
            validate_international_phonenumber,
        ]
    )

