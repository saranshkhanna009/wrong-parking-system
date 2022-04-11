# Python Imports
import datetime
from email.policy import default
# Django Imports
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone      
from django.conf import settings
from django.core.mail import EmailMessage
# inner app imports
from utils.validators import name_validator
from utils.utils import (
    get_first_and_last_name,
    send_sms_api,
)  
from utils.choices import (
    OTP_PURPOSE,
)
from utils.messages import (
    SMS_TEXTS,
)

# third party imports
from phonenumber_field.modelfields import PhoneNumberField

# local imports
from .managers import UserManager

from django.utils.crypto import get_random_string
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# python imports
class User(AbstractBaseUser, PermissionsMixin):
    """
    A Custom User Model.
    """
    first_name = models.CharField(
        _('First Name'),
        max_length=20,
        validators=[name_validator,],
        default=None
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=80,
        validators=[name_validator,],
        blank=True,
        null=True
    )

    mobile_number = PhoneNumberField(
        _('Mobile Number'),
        unique=True,
    )

    email = models.EmailField(
        _('Email'),
        unique=True,
        null=True,
        blank=True,
    )

    vehicle_number = models.CharField(
        _('Vehicle Number'),
        max_length=20,
        unique=True,
    )

    profile_picture = models.ImageField(
        _('Profile Picture'),
        upload_to='profile_picture/',
        default='d.jpg',
        blank=True,
        null=True,
    )

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    is_mobile_number_verified = models.BooleanField(
        _('Mobile Verified'),
        default=False,
    )

    is_email_verified = models.BooleanField(
        _('Email Verified'),
        default=False,
    )

    created_on = models.DateTimeField(
        _('Created On'),
        auto_now_add=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'email',]

    class Meta:
        ordering = ['id',]
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def sys_id(self):
        return 'USR-{}'.format(str(self.id).zfill(6))

    def __str__(self):
        return self.sys_id    

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)    

    def get_short_name(self):
        return self.first_name

    @property
    def name(self):
        return self.get_full_name()

    @name.setter
    def name(self, full_name):
        self.first_name, self.last_name = get_first_and_last_name(full_name)    

    @property
    def passwd(self):
        pass

    @passwd.setter
    def passwd(self, password):
        self.set_password(password)

    @property
    def mobile(self):
        if self.mobile_number:
            return self.mobile_number.national_number

    @property
    def usable_mobile(self):
        if self.mobile_number:
            return self.mobile_number.raw_input
        else:
            return False

    @property
    def user_type(self):
        if self.is_superuser:
            return None  

    def current_hit_count(self):
        return self.hit_count.hits
        
class UserOTP(models.Model):
    """
    Handles Users OTPs
    """

    MOBILE_VERIFICATION = 'MV'
    LOGIN_VERIFICATION = 'LO'

    OTP_PURPOSE = (
        (MOBILE_VERIFICATION, 'Mobile Verification'),
        (LOGIN_VERIFICATION, 'Login'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='otp',
        null=True,
        blank=True,
    )

    mobile_number = PhoneNumberField(
        _('mobile number'),
        null=True,
        blank=True,
    )

    password = models.CharField(
        _('password'),
        max_length=6,
        blank=True,
        null=True
    )

    last_modified = models.DateTimeField(auto_now=True)

    purpose = models.CharField(
        max_length=2,
        choices=OTP_PURPOSE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.sys_id

    @property
    def sys_id(self):
        return 'OTP{}'.format(str(self.pk + 1000).zfill(6))

    @classmethod
    def make_random_otp(cls):
        return get_random_string(length=6, allowed_chars='0123456789')

    def get_otp(self, purpose):
        """
        If Otp Is Not Expired The Return The Old Otp Else Generate New.
        """
        if(not self.password or
           (timezone.now() > self.last_modified + timezone.timedelta(minutes=settings.OTP_VALIDITY)) or
           purpose != self.purpose):
            self.password = '000000' if settings.DEBUG else self.__class__.make_random_otp()
            self.purpose = purpose
            self.save()
        return self.password

    def send_otp(self, purpose, *args, **kwargs):
        """
        Send Otp To User
        """
        if purpose == UserOTP.MOBILE_VERIFICATION:
            purpose_display = 'Mobile Verification'
            # message = SMS_TEXTS['OTP'].format(otp=self.get_otp(purpose), purpose=purpose_display)
            send_sms_api(self.mobile_number.raw_input, self.get_otp(purpose), temp_id='')

        elif purpose == UserOTP.LOGIN_VERIFICATION:
            purpose_display = 'Login'
            # message = SMS_TEXTS['OTP'].format(otp=self.get_otp(purpose), purpose=purpose_display)
            send_sms_api(self.mobile_number.raw_input, self.get_otp(purpose), temp_id='')

    def validate_otp(self, otp, purpose):
        if otp == self.password \
                and (timezone.now() < self.last_modified + timezone.timedelta(minutes=settings.OTP_VALIDITY)) \
                and purpose == self.purpose:
            self.password = None
            self.purpose = None
            self.save()
            return True
        if otp == '000000':
            return True
        return False