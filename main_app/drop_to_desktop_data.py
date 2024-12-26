from datetime import datetime
from django.http import HttpResponse
import openpyxl
import csv
from .models import Human, BankAccount, Card, Transaction
from django.shortcuts import redirect


# Функция генерации Excel
def generate_excel(data, file_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"

    # Заголовки
    headers = [
        'FCS', 'Credit Number', 'Credit Amount', 'Debt',
        'Credit End Date', 'Credit Status', 'Deposit Number',
        'Deposit Amount', 'Deposit End Date', 'Deposit Status'
    ]
    ws.append(headers)

    # Заполнение данными
    for row in data:
        ws.append([
            row['fcs'], row['credit_num'], row['credit_amount'], row['debt'],
            row['credit_end_date'], row['credit_status'], row['deposit_num'],
            row['deposit_amount'], row['deposit_end_date'], row['deposit_status']
        ])

    wb.save(file_path)


# Функция генерации Word
def generate_csv(data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'FCS', 'Credit Number', 'Credit Amount', 'Debt',
            'Credit End Date', 'Credit Status', 'Deposit Number',
            'Deposit Amount', 'Deposit End Date', 'Deposit Status'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        for row in data:
            writer.writerow({
                'FCS': row['fcs'],
                'Credit Number': row['credit_num'],
                'Credit Amount': row['credit_amount'],
                'Debt': row['debt'],
                'Credit End Date': row['credit_end_date'],
                'Credit Status': row['credit_status'],
                'Deposit Number': row['deposit_num'],
                'Deposit Amount': row['deposit_amount'],
                'Deposit End Date': row['deposit_end_date'],
                'Deposit Status': row['deposit_status'],
            })


# Функция для выгрузки данных
def download_data(request, type: int):
    # Создаем временные файлы
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    excel_file_path = f"C:/Users/Worker/Desktop/data_{timestamp}.xlsx"
    csv_file_path = f"C:/Users/Worker/Desktop/data_{timestamp}.csv"

    try:
        # Получаем всех людей
        humans = Human.objects.all()

        # Список для хранения всех данных
        all_data = []

        for human in humans:
            # Извлекаем все банковские счета, которые принадлежат человеку
            bank_accounts = BankAccount.objects.filter(id__in=human.bank_account_ids)

            # Извлекаем кредиты и депозиты для этих банковских счетов
            for account in bank_accounts:
                credit = None
                deposit = None

                try:
                    credit = account.credit
                except Exception as e:
                    pass

                try:
                    deposit = account.deposit
                except Exception as e:
                    pass

                # Добавляем данные в общий список
                all_data.append({
                    'fcs': human.personal_data.fcs,
                    'credit_num': credit.id if credit else None,
                    'credit_amount': credit.credit_amount if credit else None,
                    'debt': credit.debt if credit else None,
                    'credit_end_date': credit.data_end_credit if credit else None,
                    'credit_status': credit.status if credit else None,
                    'deposit_num': deposit.id if deposit else None,
                    'deposit_amount': deposit.deposit_amount if deposit else None,
                    'deposit_end_date': deposit.data_end_deposit if deposit else None,
                    'deposit_status': deposit.status if deposit else None
                })

        if type == 1:
            generate_excel(all_data, excel_file_path)
            return excel_file_path
        elif type == 2:
            generate_csv(all_data, csv_file_path)
            return csv_file_path
        else:
            raise

    except Exception as e:
        return redirect('error_page')


# Функция для выгрузки данных
def download_cards(request, type: int):
    # Создаем временные файлы
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    excel_file_path = f"C:/Users/Worker/Desktop/cards_{timestamp}.xlsx"
    csv_file_path = f"C:/Users/Worker/Desktop/cards_{timestamp}.csv"

    try:
        # Получаем всех людей
        cards = Card.objects.all()

        # Список для хранения всех данных
        all_data = []

        for card in cards:
            # Добавляем данные в общий список
            all_data.append({
                'card_number': card.number,
                'data_of_end': card.data_end_card,
                'security_code': card.security_code,
                'status': card.status
            })

        if type == 1:
            generate_excel(all_data, excel_file_path)
            return excel_file_path
        elif type == 2:
            generate_csv(all_data, csv_file_path)
            return csv_file_path
        else:
            raise

    except Exception as e:
        return redirect('error_page')


def export_data_xlsx_(request):
    download_data(request, 1)


def export_data_csv_(request):
    download_data(request, 2)


def export_cards_xlsx_(request):
    download_cards(request, 1)


def export_cards_csv_(request):
    download_cards(request, 2)
