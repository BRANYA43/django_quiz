from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView,  PasswordResetCompleteView,  \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns_accounts = [
    path('change/', PasswordChangeView.as_view(), name='password_change'),
    path('change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include(urlpatterns_accounts)),
    path('quiz/', include('quiz.urls')),
    path('tasks/', include('long_task.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
