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
    path('admin/', admin.site.urls),  # Админ панель будет доступна по /admin/
    path('user_login/', views.user_login, name='user_login'),  # Вход для клиента
    path('worker_dashboard/', views.employee_dashboard, name='worker_dashboard'),  # Рабочая панель
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),  # Клиентская панель
    path('add_transaction/', views.add_transaction, name='add_transaction'),  # Добавить транзакцию
    path('edit_credit/', views.edit_credit, name='edit_credit'),  # Обновить данные по кредиту
    path('edit_deposit/', views.edit_deposit, name='edit_deposit'),  # Обновить данные по кредиту
    path('open_credit/', views.open_credit, name='open_credit'),  # Создать кредит
    path('open_deposit/', views.open_deposit, name='open_deposit'),  # Создать депозит
    path('open_card/', views.open_card, name='open_card'),  # Создать карту
    path('close_card/', views.close_card, name='close_card'),  # Закрыть карту
    path('view_user_accounts/', views.view_user_accounts, name='view_user_accounts'), # Посмотреть
                                                                                      # данные о пользователях
    path('error/', views.error_page, name='error_page'),  # Страница ошибки
]
