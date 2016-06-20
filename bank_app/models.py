from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Transaction(models.Model):
    type_choices = (('+', 'Deposit'), ('-', 'Debit'))
    user = models.ForeignKey(User)
    transaction_type = models.CharField(max_length=6, choices=type_choices)
    date = models.DateTimeField(auto_now_add=True)
    ammount = models.DecimalField(max_digits=8, decimal_places=2)
    payee = models.CharField(max_length=50)

    def __str__(self):
        return self.payee
