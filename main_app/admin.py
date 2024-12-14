from django.contrib import admin
from .models import PersonalData, OrganizationData, Human, BankAccount, Credit, Deposit, Card, Transaction

admin.site.register(PersonalData)
admin.site.register(OrganizationData)
admin.site.register(Human)
admin.site.register(BankAccount)
admin.site.register(Credit)
admin.site.register(Deposit)
admin.site.register(Card)
admin.site.register(Transaction)
