from django.urls import path
from django.views.decorators.cache import cache_page

from long_task.views import get_status, run_task, home


app_name = 'long_tasks'

urlpatterns = [
    # path('home/', cache_page(timeout=30)(home), name='home'),
    path('home/', home, name='home'),
    path('<task_id>/', get_status, name='status'),
    path('', run_task, name='run'),
]