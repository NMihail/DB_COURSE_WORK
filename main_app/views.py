from django.shortcuts import render, redirect
from .models import Human, PersonalData  # Импорт моделей


# Главная страница
def index(request):
    return render(request, 'main_app/index.html')


# Вход для работника
def employee_login(request):
    if request.method == 'POST':
        passport_series = request.POST.get('passport_series')
        passport_number = request.POST.get('passport_number')

        try:
            # Проверяем персональные данные
            personal_data = PersonalData.objects.get(
                passport_series=passport_series,
                passport_number=passport_number
            )

            # Проверяем, является ли человек работником
            human = Human.objects.get(personal_data=personal_data)
            if human.employee_credit_organization:
                # Успешный вход для работника
                return redirect('worker_dashboard')
            else:
                # Человек не является работником
                return redirect('error_page')

        except (PersonalData.DoesNotExist, Human.DoesNotExist):
            # Персональные данные или запись в Human не найдены
            return redirect('error_page')

    return render(request, 'main_app/employee_login.html')


# Вход для клиента
def client_login(request):
    if request.method == 'POST':
        passport_series = request.POST.get('passport_series')
        passport_number = request.POST.get('passport_number')

        try:
            # Проверяем персональные данные
            personal_data = PersonalData.objects.get(
                passport_series=passport_series,
                passport_number=passport_number
            )

            # Проверяем, является ли человек клиентом
            human = Human.objects.get(personal_data=personal_data)
            if not human.employee_credit_organization:
                # Успешный вход для клиента
                return redirect('client_dashboard')
            else:
                # Человек является работником, но пытается войти как клиент
                return redirect('error_page')

        except (PersonalData.DoesNotExist, Human.DoesNotExist):
            # Персональные данные или запись в Human не найдены
            return redirect('error_page')

    return render(request, 'main_app/client_login.html')


# Рабочая панель для работника
def worker_dashboard(request):
    return render(request, 'main_app/worker_dashboard.html')


# Клиентская панель
def client_dashboard(request):
    return render(request, 'main_app/client_dashboard.html')


# Страница ошибки
def error_page(request):
    return render(request, 'main_app/error_page.html', {
        'error_message': 'Ошибка! Убедитесь в правильности введённых данных.'
    })
