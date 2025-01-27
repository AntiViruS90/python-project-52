from django.urls import include, path

app_name = 'Task_Manager.api'

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('Task_Manager.api.users_api.urls')),
]
