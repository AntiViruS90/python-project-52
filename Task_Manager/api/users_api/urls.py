from django.urls import path

from . import api_views

app_name = 'Task_Manager.api.users_api'

urlpatterns = [
    path('users/', api_views.UsersAPIList.as_view(), name='users_api'),
    path('users/<int:pk>/', api_views.UsersAPIUpdateDestroy.as_view()),
]
