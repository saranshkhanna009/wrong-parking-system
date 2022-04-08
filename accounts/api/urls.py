#python imports

#django imports
from django.urls import re_path, include

#third-party imports

#inter-app imports

#local imports


urlpatterns = [
   re_path(r'^v1/', include('accounts.api.v1.urls')),
]
