# Generated by Django 5.1.4 on 2024-12-22 21:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('money_amount', models.BigIntegerField()),
            ],
            options={
                'db_table': 'bank_account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('data_end_card', models.DateField()),
                ('security_code', models.CharField(max_length=10)),
                ('status', models.BooleanField()),
            ],
            options={
                'db_table': 'card',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_amount', models.BigIntegerField()),
                ('debt', models.BigIntegerField()),
                ('data_end_credit', models.DateField()),
                ('status', models.BooleanField()),
            ],
            options={
                'db_table': 'credit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_amount', models.BigIntegerField()),
                ('data_end_deposit', models.DateField()),
                ('status', models.BooleanField()),
            ],
            options={
                'db_table': 'deposit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_account_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('employee_credit_organization', models.BooleanField()),
                ('organization', models.BooleanField()),
            ],
            options={
                'db_table': 'human',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('inn', models.CharField(max_length=50)),
                ('ogrn', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'organization_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_series', models.CharField(max_length=50)),
                ('passport_number', models.CharField(max_length=50)),
                ('inn', models.CharField(max_length=50)),
                ('fcs', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'personal_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.BooleanField()),
                ('money_amount', models.BigIntegerField()),
                ('status', models.BooleanField()),
            ],
            options={
                'db_table': 'transaction',
                'managed': False,
            },
        ),
    ]
