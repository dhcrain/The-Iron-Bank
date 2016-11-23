from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Transaction(models.Model):
    type_choices = (('+', 'Deposit'), ('-', 'Debit'))
    user = models.ForeignKey(User)
    transaction_type = models.CharField(max_length=6, choices=type_choices)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payee = models.CharField(max_length=50)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.payee


class Profile(models.Model):
    user = models.OneToOneField(User)

    @property
    def get_balance(self):
        user = User.objects.get(id=self.user_id)
        acct_balance = 0
        transactions = Transaction.objects.filter(user=user)
        for trans in transactions:
            if trans.transaction_type == '+':
                acct_balance += trans.amount
            else:
                acct_balance -= trans.amount
        return round(acct_balance, 2)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")
    if created:
        Profile.objects.create(user=instance)
