from django.shortcuts import (
    render,
    redirect,
)
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
    RedirectView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from utils.mixins import (
    LoginNotRequiredMixin, 
)
from utils.messages import SMS_TEXTS, SYSTEM_SUCCESS_MESSAGE, SYSTEM_ERROR_MESSAGE
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordChangeView,
    LoginView,
)
from .forms import UserForm, AuthenticationForm, ProfileForm
from django.urls import (
    reverse_lazy, 
    reverse,
)
from django.contrib.messages.views import SuccessMessageMixin
import logging
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.views import generic
from django.contrib import messages
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect
from hitcount.views import HitCountDetailView
from django.views.generic.edit import DeleteView

User = get_user_model()

class RegisterView(CreateView):
    model = User  
    form_class = UserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

class LoginView(LoginView):
    """
    Login view
    """
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:profile_detail')

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

class LogoutView(RedirectView):
    """
    It will Logout User And Redirect User To Login Page After Logout
    """
    pattern_name = 'accounts:login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(self.__class__, self).get(request, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Profile detail view
    """

    template_name = 'accounts/profile.html'
    
    def get_template_names(self):
        return super(self.__class__, self).get_template_names()

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    """
    profile Update View
    """

    template_name = 'accounts/profile_form.html'
    
    def get_object(self):
        return self.request.user

    def get_template_names(self):
        return super(self.__class__, self).get_template_names()

    def get_success_url(self):
        return reverse('accounts:profile_detail', kwargs={})

    def get_context_data(self, *args, **kwargs):
        context = super(self.__class__, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context['user_form'] = ProfileForm(instance=user)
        return context

    def post(self, request, *args, **kwargs):

        user_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.get_object(),)

        if user_form.is_valid():
            user_form.save()
            messages.success(self.request, SYSTEM_SUCCESS_MESSAGE['PROFILE_UPDATE'])

            return redirect(self.get_success_url())

        context = {
            'user_form': user_form,
        } 
        return self.render_to_response(context)

class QrCodeProfileView(HitCountDetailView):
    """
    QrCode Profile view
    """
    model = User
    template_name = 'accounts/qr_code_profile.html'
    raise_exception = True 
    count_hit = True
    
    def get_context_data(self, **kwargs):
        context = super(QrCodeProfileView, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': User.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context