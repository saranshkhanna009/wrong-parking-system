# django imports
from re import I
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# inner app imports
from utils.validators import name_validator
from utils.utils import get_first_and_last_name
from .models import UserOTP
from phonenumber_field.formfields import PhoneNumberField
# from django.utils.http import is_safe_url
from is_safe_url import is_safe_url
from wrong_parking_system.messages import VALIDATION_ERROR_MESSAGES
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
User = get_user_model()

class UserForm(forms.ModelForm):
    """
    user registration form
    """
    otp = forms.CharField(label='OTP', max_length=6)
    password1 = None
    password2 = None

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'vehicle_number',
            'mobile_number',
            'otp',
        )

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].initial = '+91'
        self.fields['first_name'].widget.attrs["class"] = 'form-control'
        self.fields['last_name'].widget.attrs["class"] = 'form-control'
        self.fields['vehicle_number'].widget.attrs["class"] = 'form-control'
        self.fields['mobile_number'].widget.attrs["class"] = 'form-control'
        self.fields['otp'].widget.attrs["class"] = 'form-control'

    def clean(self):
        """Validate cleaned data"""
        cleaned_data = super(self.__class__, self).clean()
        error_dict = {}

        otp = cleaned_data.get('otp')
        mobile_number = cleaned_data.get('mobile_number')
        try:
            otp_user = UserOTP.objects.get(mobile_number=mobile_number)
            if not otp_user.validate_otp(otp, UserOTP.MOBILE_VERIFICATION):
                error_dict['otp'] = 'OTP Is not Valid'
        except:
            error_dict['otp'] = 'OTP Is not Valid'

        if error_dict:
            raise forms.ValidationError(error_dict)

        return cleaned_data

    def save(self, commit=True):
        user = super(self.__class__, self).save(commit=False)
        mobile_number = self.cleaned_data["mobile_number"]
        otp = UserOTP.objects.filter(mobile_number=mobile_number)[0]

        if commit:
            user.save()
            otp.user = user
            otp.save()

        return user



class AuthenticationForm(AuthenticationForm):
    """
    authentication form
    """

    username = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'}),
        initial="+91",
        required=True,
        max_length=13
    )

    otp = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'OTP', 'class': 'form-control'}),
        required=True,
        max_length=6,
        min_length=6
    )
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'otp',
        )

    def __init__(self, request=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['username'].initial = '+91'
        self.fields['otp'].widget.attrs["class"] = 'form-control'

    def clean(self, request=None):
        """Validate cleaned data"""
        cleaned_data = super(self.__class__, self).clean()

        otp = cleaned_data.get('otp')
        username = cleaned_data.get('username')
        if otp:
            self.user_cache = authenticate(self.request, mobile_number=username, otp=otp)
            if self.user_cache is None:
                raise forms.ValidationError(
                    VALIDATION_ERROR_MESSAGES['INVALID_OTP']
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return cleaned_data

class ProfileForm(forms.ModelForm):
    """
    Profile Update Form
    """
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'vehicle_number',
            'profile_picture',
        )

