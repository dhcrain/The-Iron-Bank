from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Transaction(models.Model):
    type_choices = (('+', 'Credit'), ('-', 'Debit'))
    user = models.ForeignKey(User)
    transaction_type = models.CharField(max_length=6, choices=type_choices)
    date = models.DateTimeField(auto_now_add=True)
    ammount = models.FloatField()
    payee = models.CharField(max_length=50)
