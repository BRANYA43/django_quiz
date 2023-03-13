from django.urls import path
from django.views.generic import TemplateView

from .views import UserLoginView, UserLogoutView, UserProfileUpdateView, UserReactivationView, UserRegisterView, \
    user_activate, user_profile_view


app_name = 'accounts'

urlpatterns = [
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', TemplateView.as_view(template_name='accounts/user_register_done.html'), name='register_done'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', user_profile_view, name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('reactivation/', UserReactivationView.as_view(), name='reactivation'),
    path('reactivation/done', TemplateView.as_view(template_name='accounts/user_reactivation_done.html'),
         name='reactivation_done'),
]
