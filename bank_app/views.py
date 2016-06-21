from django.shortcuts import render
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from bank_app.models import Transaction
from django.http import request
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

# Create your views here.

def get_balance(self):
    self.acct_balance = 0
    transactions = Transaction.objects.filter(user=self.request.user)
    for trans in transactions:
        if trans.transaction_type == '+':
            self.acct_balance += trans.ammount
        else:
            self.acct_balance -= trans.ammount
    return self.acct_balance


class IndexView(TemplateView):
    template_name = "index.html"


class AccountView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'bank_app/transaction_list.html'

    transaction = Transaction.objects.all()
    for trans in transaction:
        print(trans.transaction_type)

    def get_context_data(self, **kwargs):
        get_balance(self)
        context = super().get_context_data(**kwargs)
        context["balance"] = self.acct_balance
        thirty_days_ago = datetime.datetime.now() + datetime.timedelta(days=-30)
        context['transactions'] = Transaction.objects.filter(user=self.request.user).filter(date__gt=thirty_days_ago)
        return context

class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# can't navigate to, will impliment in part 2, cant get the <0 finction to work, and its late.
class AddTransactionView(CreateView):
    model = Transaction
    fields = ['transaction_type', 'ammount', 'payee']
    success_url = '/account'

    def form_valid(self, form):
        context = super().get_context_data()
        get_balance(self)
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        if transaction.transaction_type == '-':
            if (self.acct_balance - transaction.ammount) <= 0:
                success_url = '/account'
                context['not_allowed'] = "Insufficient Funds"
                return context

        return super(AddTransactionView, self).form_valid(form)
