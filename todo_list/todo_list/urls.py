"""
URL configuration for todo_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.open),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('task', views.tasks, name='task'),
    path('add-task', views.todo, name='add_task'),
    path('mark-done/<int:task_id>/', views.mark_done, name='mark_done'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('logout',views.logout, name='logout'),
]
