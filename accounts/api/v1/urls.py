# python imports

# django imports

from os import name
from django.urls import path
# from django.conf.urls import url
from django.urls import re_path

# third party imports
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import (
    GenerateOtpAPIView,
    # ValidateOtpAPIView,
    # ValidateUserTokenApiView,
)

urlpatterns = [

    re_path(r'^generate-otp$', GenerateOtpAPIView.as_view(), name='generate_otp'),
    # re_path(r'^validate-otp$', ValidateOtpAPIView.as_view(), name='validate_otp'),
    # re_path(r'^validate-token$', ValidateUserTokenApiView.as_view(), name='validate_token'),
   
]

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)

