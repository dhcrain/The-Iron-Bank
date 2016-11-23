from django.contrib import admin
from bank_app.models import Transaction, Profile
# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'transaction_type', 'amount', 'payee')

admin.site.register(Transaction, TransactionAdmin)

admin.site.register(Profile)
