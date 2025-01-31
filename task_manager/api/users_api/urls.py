from django.urls import path

from . import api_views

app_name = 'task_manager.api.users_api'

urlpatterns = [
    path('users/', api_views.UsersAPIList.as_view(), name='users_api'),
    path('users/<int:pk>/', api_views.UsersAPIUpdateDestroy.as_view()),
]
