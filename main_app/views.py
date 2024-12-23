import random
from django.shortcuts import render, redirect
from .models import Human, PersonalData, BankAccount, Transaction, Credit, Deposit, Card  # Импорт моделей


# Главная страница
def index(request):
    return render(request, 'main_app/index.html')


# Вход для работника
def employee_login(request):
    if request.method == 'POST':
        passport_series = request.POST.get('passport_series')
        passport_number = request.POST.get('passport_number')

        try:
            personal_data = PersonalData.objects.get(
                passport_series=passport_series,
                passport_number=passport_number
            )

            human = Human.objects.get(personal_data=personal_data)
            if human.employee_credit_organization:
                # Сохраняем ID работника в сессии
                request.session['employee_id'] = human.id
                return redirect('worker_dashboard')
            else:
                return redirect('error_page')

        except (PersonalData.DoesNotExist, Human.DoesNotExist):
            return redirect('error_page')

    return render(request, 'main_app/employee_login.html')


# Рабочая панель для работника
def employee_dashboard(request):
    return render(request, 'main_app/worker_dashboard.html')


def add_transaction(request):
    if request.method == 'POST':
        # Получаем данные из формы
        account_out_number = request.POST.get('account_out')  # Номер счета отправителя
        account_in_number = request.POST.get('account_in')  # Номер счета получателя
        money_amount = float(request.POST.get('money_amount'))  # Сумма перевода
        payment_method = request.POST.get('payment_method') == 'True'  # Метод оплаты

        try:
            # Получаем счета отправителя и получателя
            account_out = BankAccount.objects.get(number=account_out_number)
            account_in = BankAccount.objects.get(number=account_in_number)

            # Проверяем доступность средств на счете отправителя
            if account_out.money_amount < money_amount:
                return redirect('add_transaction')

            # Выполняем перевод средств между счетами
            account_out.money_amount -= money_amount
            account_in.money_amount += money_amount

            # Сохраняем обновленные данные
            account_out.save()
            account_in.save()

            # Создаем запись о транзакции
            Transaction.objects.create(
                payment_method=payment_method,  # Указанный метод оплаты
                bank_account_out=account_out,
                bank_account_in=account_in,
                money_amount=money_amount,
                status=True  # Успешная транзакция
            )

            # Сообщаем об успешной транзакции
            return redirect('worker_dashboard')

        except BankAccount.DoesNotExist:
            return redirect('add_transaction')

    return render(request, 'main_app/add_transaction.html')


def edit_credit(request):
    if request.method == 'POST':
        # Получаем данные из формы
        account_number = request.POST.get('account_number')  # Номер счета
        new_credit_amount = request.POST.get('credit_amount')  # Новая сумма кредита
        new_debt = request.POST.get('debt')  # Новый долг
        new_data_end_credit = request.POST.get('data_end_credit')  # Новая дата окончания кредита
        new_status = request.POST.get('status') == 'True'  # Новый статус (True/False)

        try:
            # Находим счет по номеру
            account = BankAccount.objects.get(number=account_number)

            # Проверяем, привязан ли к счету кредит
            if not account.credit:
                return redirect('edit_credit')

            # Редактируем данные кредита
            credit = account.credit
            if new_credit_amount:
                credit.credit_amount = new_credit_amount
            if new_debt:
                credit.debt = new_debt
            if new_data_end_credit:
                credit.data_end_credit = new_data_end_credit
            credit.status = new_status

            # Сохраняем изменения
            credit.save()

            return redirect('worker_dashboard')

        except BankAccount.DoesNotExist:
            return redirect('edit_credit')

    return render(request, 'main_app/edit_credit.html')


def edit_deposit(request):
    if request.method == 'POST':
        # Получаем данные из формы
        account_number = request.POST.get('account_number')  # Номер банковского счета
        new_deposit_amount = request.POST.get('deposit_amount')  # Новая сумма депозита
        new_data_end_deposit = request.POST.get('data_end_deposit')  # Новая дата окончания депозита
        new_status = request.POST.get('status') == 'True'  # Новый статус (True/False)

        try:
            # Находим банковский аккаунт по номеру
            account = BankAccount.objects.get(number=account_number)

            # Проверяем, что этот счет связан с депозитом
            if not account.deposit:
                return redirect('edit_deposit')

            # Редактируем данные депозита
            deposit = account.deposit
            if new_deposit_amount:
                deposit.deposit_amount = new_deposit_amount
            if new_data_end_deposit:
                deposit.data_end_deposit = new_data_end_deposit
            deposit.status = new_status

            # Сохраняем изменения
            deposit.save()

            return redirect('worker_dashboard')

        except BankAccount.DoesNotExist:
            return redirect('edit_deposit')

    return render(request, 'main_app/edit_deposit.html')


def generate_unique_account_number():
    """Генерирует уникальный номер банковского счета."""
    while True:
        # Генерация 20-значного номера счета
        account_number = str(random.randint(10 ** 20, 10 ** 21 - 1))
        # Проверка уникальности
        if not BankAccount.objects.filter(number=account_number).exists():
            return account_number


def open_credit(request):
    if request.method == 'POST':
        # Получение данных из формы
        human_id = request.POST.get('human_id')  # ID пользователя (человека)
        credit_amount = request.POST.get('credit_amount')  # Сумма кредита
        debt = request.POST.get('debt')  # Долг по кредиту
        data_end_credit = request.POST.get('data_end_credit')  # Дата окончания кредита
        status = request.POST.get('status') == 'True'  # Статус кредита

        try:
            # Проверяем, существует ли пользователь с указанным ID
            human = Human.objects.get(id=human_id)

            # Генерируем уникальный номер банковского счета
            account_number = generate_unique_account_number()

            # Создаем запись для нового кредита
            credit = Credit.objects.create(
                credit_amount=credit_amount,
                debt=debt,
                data_end_credit=data_end_credit,
                status=status
            )

            # Создаем банковский аккаунт, связанный с этим кредитом
            bank_account = BankAccount.objects.create(
                number=account_number,
                credit=credit,
                money_amount=credit_amount
            )

            # Добавляем ID созданного счета в список банковских счетов пользователя
            human.bank_account_ids.append(bank_account.id)
            human.save()

            return redirect('worker_dashboard')

        except Human.DoesNotExist:
            return redirect('open_credit')

        except Exception as e:
            return redirect('open_credit')

    return render(request, 'main_app/open_credit.html')


def open_deposit(request):
    if request.method == 'POST':
        # Получение данных из формы
        human_id = request.POST.get('human_id')  # ID пользователя (человека)
        deposit_amount = request.POST.get('deposit_amount')  # Сумма депозита
        data_end_deposit = request.POST.get('data_end_deposit')  # Дата окончания депозита
        status = request.POST.get('status') == 'True'  # Статус депозита

        try:
            # Проверяем, существует ли пользователь с указанным ID
            human = Human.objects.get(id=human_id)

            # Генерируем уникальный номер банковского счета
            account_number = generate_unique_account_number()

            # Создаем запись для нового депозита
            deposit = Deposit.objects.create(
                deposit_amount=deposit_amount,
                data_end_deposit=data_end_deposit,
                status=status
            )

            # Создаем банковский аккаунт, связанный с этим депозитом
            bank_account = BankAccount.objects.create(
                number=account_number,
                deposit=deposit,
                money_amount=deposit_amount  # Сумма депозита становится балансом
            )

            # Добавляем ID созданного счета в список банковских счетов пользователя
            human.bank_account_ids.append(bank_account.id)
            human.save()

            return redirect('worker_dashboard')

        except Human.DoesNotExist:
            return redirect('open_deposit')

        except Exception as e:
            return redirect('open_deposit')

    return render(request, 'main_app/open_deposit.html')


def generate_unique_card_number():
    """Генерирует уникальный номер карты."""
    while True:
        # Генерация 16-значного номера карты
        card_number = str(random.randint(10 ** 15, 10 ** 16 - 1))
        # Проверка уникальности
        if not Card.objects.filter(number=card_number).exists():
            return card_number


def open_card(request):
    if request.method == 'POST':
        # Получение данных из формы
        bank_account_id = request.POST.get('bank_account_id')  # ID банковского аккаунта
        data_end_card = request.POST.get('data_end_card')  # Дата окончания карты
        security_code = str(random.randint(100, 999))  # Генерация CVV кода
        status = request.POST.get('status') == 'True'  # Статус карты

        try:
            # Проверяем, существует ли банковский аккаунт
            bank_account = BankAccount.objects.get(id=bank_account_id)

            # Генерируем уникальный номер карты
            card_number = generate_unique_card_number()

            # Создаем новую карту
            card = Card.objects.create(
                number=card_number,
                data_end_card=data_end_card,
                security_code=security_code,
                bank_account=bank_account,
                status=status
            )

            return redirect('worker_dashboard')

        except BankAccount.DoesNotExist:
            return redirect('open_card')

        except Exception as e:
            return redirect('open_card')

    return render(request, 'main_app/open_card.html')


def close_card(request):
    if request.method == 'POST':
        # Получение данных из формы
        card_number = request.POST.get('card_number')  # Номер карты

        try:
            # Находим карту по номеру
            card = Card.objects.get(number=card_number)

            # Изменяем статус карты на "Неактивна"
            card.status = False
            card.save()

            return redirect('worker_dashboard')

        except Card.DoesNotExist:
            return redirect('close_card')

        except Exception as e:
            return redirect('close_card')

    return render(request, 'main_app/close_card.html')


def view_user_accounts(request):
    if request.method == 'POST':
        passport_series = request.POST.get('passport_series')
        passport_number = request.POST.get('passport_number')

        try:
            # Находим персональные данные по паспорту
            personal_data = PersonalData.objects.get(
                passport_series=passport_series,
                passport_number=passport_number
            )

            # Находим человека, связанного с этим паспортом
            human = Human.objects.get(personal_data=personal_data)

            # Получаем все банковские счета для этого человека
            bank_accounts = BankAccount.objects.filter(id__in=human.bank_account_ids)

            accounts_info = []
            for account in bank_accounts:
                # Для каждого счета проверяем, есть ли связанные кредиты или депозиты
                credit = account.credit if account.credit else None
                deposit = account.deposit if account.deposit else None

                accounts_info.append({
                    'account': account,
                    'credit': credit,
                    'deposit': deposit
                })

            return render(request, 'main_app/view_user_accounts.html', {'accounts_info': accounts_info})

        except PersonalData.DoesNotExist:
            return redirect('worker_dashboard')

        except Human.DoesNotExist:
            return redirect('worker_dashboard')

    return render(request, 'main_app/view_user_accounts.html')


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
                # Сохраняем данные в сессии
                request.session['human_id'] = human.id

                # Успешный вход для клиента
                return redirect('client_dashboard')
            else:
                # Человек является работником, но пытается войти как клиент
                return redirect('error_page')

        except (PersonalData.DoesNotExist, Human.DoesNotExist):
            # Персональные данные или запись в Human не найдены
            return redirect('error_page')

    return render(request, 'main_app/client_login.html')


# Клиентская панель с информацией о банковских счетах, кредитах и депозитах
def client_dashboard(request):
    human_id = request.session.get('human_id')  # Получаем ID человека из сессии
    if not human_id:
        return redirect('client_login')

    try:
        human = Human.objects.get(id=human_id)  # Загружаем объект Human

        # Получаем связанные банковские счета по ID
        bank_accounts = BankAccount.objects.filter(id__in=human.bank_account_ids)

        # Собираем дополнительную информацию о кредитах и депозитах
        accounts_data = []
        for account in bank_accounts:
            account_info = {
                'number': account.number,
                'money_amount': account.money_amount,
                'credit': None,
                'deposit': None,
            }
            if account.credit:
                account_info['credit'] = {
                    'credit_amount': account.credit.credit_amount,
                    'debt': account.credit.debt,
                    'data_end_credit': account.credit.data_end_credit,
                    'status': account.credit.status,
                }
            if account.deposit:
                account_info['deposit'] = {
                    'deposit_amount': account.deposit.deposit_amount,
                    'data_end_deposit': account.deposit.data_end_deposit,
                    'status': account.deposit.status,
                }
            accounts_data.append(account_info)

    except Human.DoesNotExist:
        return redirect('client_login')

    return render(request, 'main_app/client_dashboard.html', {
        'human': human,
        'accounts_data': accounts_data,
    })


# Страница ошибки
def error_page(request):
    return render(request, 'main_app/error_page.html', {
        'error_message': 'Ошибка! Убедитесь в правильности введённых данных.'
    })
