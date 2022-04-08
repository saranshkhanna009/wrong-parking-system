from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class LoginNotRequiredMixin(AccessMixin):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:login')
        return super(LoginNotRequiredMixin, self).get(request, *args, **kwargs)

