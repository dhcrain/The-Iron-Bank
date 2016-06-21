from django.shortcuts import render
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from bank_app.models import Transaction
from django.http import request
from django.contrib.auth.models import User

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

class AccountView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'bank_app/transaction_list.html'

    transaction = Transaction.objects.all()
    for trans in transaction:
        print(trans.transaction_type)

    def get_context_data(self, **kwargs):
        acct_balance = 0
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.filter(user=self.request.user)
        for trans in transactions:
            if trans.transaction_type == '+':
                acct_balance += trans.ammount
            else:
                acct_balance -= trans.ammount
        context["balance"] = acct_balance
        context['transactions'] = Transaction.objects.filter(user=self.request.user).filter(date__lte=datetime.datetime.today(), date__gt=datetime.datetime.today()-datetime.timedelta(days=30))
        return context

class DetailView(TemplateView):
    model = Transaction
    template_name = 'transaction_detail.html'

    def get_context_data(self, **kwargs):
        trans_pk = self.kwargs.get('pk', None)      # gets Bookmark PK
        context = super().get_context_data(**kwargs)    # I have no idea what this does
        context["transaction"] = Transaction.objects.get(id=trans_pk)
        # context["clicks"] = Click.objects.filter(link=bookmark_pk)
        return context
