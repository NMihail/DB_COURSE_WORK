from django.db import models
from django.contrib.postgres.fields import ArrayField


# Модель для таблицы personal_data
class PersonalData(models.Model):
    passport_series = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=50)
    inn = models.CharField(max_length=50)
    fcs = models.CharField(max_length=100)

    class Meta:
        db_table = 'personal_data'  # указываем имя таблицы в БД
        managed = False

    def __str__(self):
        return f'{self.passport_series} {self.passport_number}'


# Модель для таблицы organization_data
class OrganizationData(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(PersonalData, on_delete=models.CASCADE, related_name='led_organizations')
    inn = models.CharField(max_length=50)
    ogrn = models.CharField(max_length=50)

    class Meta:
        db_table = 'organization_data'
        managed = False

    def __str__(self):
        return self.name


# Модель для таблицы human
class Human(models.Model):
    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE, related_name='humans')
    organization_data = models.ForeignKey(OrganizationData, on_delete=models.CASCADE, related_name='employees')
    bank_account_ids = ArrayField(models.IntegerField(), blank=True, default=list)
    employee_credit_organization = models.BooleanField()  # Новый столбец
    organization = models.BooleanField()  # Новый столбец

    class Meta:
        db_table = 'human'
        managed = False

    def __str__(self):
        return f'{self.personal_data} - {self.organization_data}'


# Модель для таблицы bank_account
class BankAccount(models.Model):
    number = models.CharField(max_length=50)
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, null=True, blank=True)
    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE, null=True, blank=True)
    money_amount = models.BigIntegerField()
    card = models.ForeignKey('Card', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'bank_account'
        managed = False

    def __str__(self):
        return self.number


# Модель для таблицы credit
class Credit(models.Model):
    credit_amount = models.BigIntegerField()
    debt = models.BigIntegerField()
    data_end_credit = models.DateField()
    status = models.BooleanField()

    class Meta:
        db_table = 'credit'
        managed = False

    def __str__(self):
        return f'Credit {self.id}'


# Модель для таблицы deposit
class Deposit(models.Model):
    deposit_amount = models.BigIntegerField()
    data_end_deposit = models.DateField()
    status = models.BooleanField()

    class Meta:
        db_table = 'deposit'
        managed = False

    def __str__(self):
        return f'Deposit {self.id}'


# Модель для таблицы card
class Card(models.Model):
    number = models.CharField(max_length=50)
    data_end_card = models.DateField()
    security_code = models.CharField(max_length=10)
    bank_account = models.ForeignKey(
        'BankAccount',
        on_delete=models.CASCADE,
        related_name='cards'  # Изменено с 'card' на 'cards'
    )
    status = models.BooleanField()

    class Meta:
        db_table = 'card'
        managed = False

    def __str__(self):
        return self.number


# Модель для таблицы transaction
class Transaction(models.Model):
    payment_method = models.BooleanField()  # Можно использовать BooleanField для способа оплаты
    bank_account_out = models.ForeignKey(BankAccount, related_name='transactions_out', on_delete=models.CASCADE)
    bank_account_in = models.ForeignKey(BankAccount, related_name='transactions_in', on_delete=models.CASCADE)
    money_amount = models.BigIntegerField()
    status = models.BooleanField()

    class Meta:
        db_table = 'transaction'
        managed = False

    def __str__(self):
        return f'Transaction {self.id}'
