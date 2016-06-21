from django.shortcuts import render
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
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
        context['transactions'] = Transaction.objects.filter(user=self.request.user).filter(date__lte=datetime.datetime.today(), date__gt=datetime.datetime.today()-datetime.timedelta(days=30))
        return context

class DetailView(LoginRequiredMixin, TemplateView):
    model = Transaction
    template_name = 'transaction_detail.html'

    def get_context_data(self, **kwargs):
        trans_pk = self.kwargs.get('pk', None)
        trans = Transaction.objects.get(id=trans_pk)
        context = super().get_context_data(**kwargs)    # I have no idea what this does
        if self.request.user == trans.user:
            context["transaction"] = trans
        else:
            context["not_auth"] = "You are not authorized to view this data."
        return context

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
