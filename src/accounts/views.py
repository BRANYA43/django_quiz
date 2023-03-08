from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import UserRegisterForm, UserUpdateForm
from accounts.utils import signer


class UserRegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/user_register.html'
    success_url = reverse_lazy('accounts:register_done')
    form_class = UserRegisterForm


def user_activate(request, sign):
    try:
        username = signer.usingn(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')

    user = get_object_or_404(get_user_model(), username=username)
    if user.is_active:
        templates = 'accounts/user_is_activated.html'
    else:
        templates = 'accounts/user_activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, templates)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/user_logout.html'


@login_required
def user_profile_view(request):
    return render(request, 'accounts/user_profile.html')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_profile_update.html'
    model = get_user_model()
    success_url = reverse_lazy('accounts:profile')
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user