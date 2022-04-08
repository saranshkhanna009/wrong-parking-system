# python imports

# django imports

from django.urls import path, include
# from django.contrib.auth.views import LogoutView

# local imports
from .views import (
    LoginView,
    ProfileDetailView,
    ProfileUpdateView,
    RegisterView,
    LogoutView,
    QrCodeProfileView,
)

app_name = 'accounts'

urlpatterns = [

    path('api/', include('accounts.api.urls')), # apis

    # authentication related urls
    path('', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name="register"),

    # profile urls
    path('profile/detail', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile_update'), 

    #qr-code profile urls
    path('qr-code/<int:pk>/profile', QrCodeProfileView.as_view(), name='qr_code_profile'),  
]