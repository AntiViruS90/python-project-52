"""
URL configuration for Task_Manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Task_Manager.task_manager_main.urls', namespace='main')),
    path('users/', include('Task_Manager.users.urls', namespace='users')),
    path(
        'statuses', include('Task_Manager.statuses.urls', namespace='statuses')
    ),
    path('tasks/', include('Task_Manager.tasks.urls', namespace='tasks')),
    path(
        'labels/', include('Task_Manager.labels.urls', namespace='labels')
    ),
    path('api/v1/', include('Task_Manager.api.urls')),
    path('api/v1/', include('rest_framework.urls', namespace='rest_framework')),
]
