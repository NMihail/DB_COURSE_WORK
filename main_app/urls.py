"""
URL configuration for main_app project.

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('employee_login/', views.employee_login, name='employee_login'),  # Вход для работника
    path('client_login/', views.client_login, name='client_login'),  # Вход для клиента
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),  # Рабочая панель
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),  # Клиентская панель
    path('error/', views.error_page, name='error_page'),  # Страница ошибки
]
