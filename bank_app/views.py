from django.shortcuts import render
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from bank_app.models import Transaction
from bank_app.forms import TransferForm
from django.http import request, HttpResponse
from django.db.models.base import ObjectDoesNotExist

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


class AddTransactionView(CreateView):
    model = Transaction
    fields = ['transaction_type', 'ammount', 'payee']
    success_url = '/account'

    def form_valid(self, form):
        context = super().get_context_data()
        transaction = form.save(commit=False)

    def form_valid(self, form):
        context = super().get_context_data()
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        if transaction.transaction_type == '-':
            balance = get_balance(self)
            if (balance - transaction.ammount) <= 0:
                return HttpResponse("Insufficient Funds, you only have $" + str(balance) + " avalible.")
        return super().form_valid(form)

class TransferView(CreateView):
    model = Transaction
    fields = ['payee', 'ammount']
    # form_class = TransferForm
    template_name = 'bank_app/transfer.html'
    success_url = '/account'


    def form_valid(self, form):
        context = super().get_context_data()
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.transaction_type='-'
        balance = get_balance(self)


        try:
            User.objects.get(id=transaction.payee)
            if int(self.request.user.id) == int(transaction.payee):
                return HttpResponse("Why are you trying to trasfer money to yourself?")
        except ObjectDoesNotExist:
            return HttpResponse("That account does not exist")


        if (balance - transaction.ammount) <= 0:
            return HttpResponse("Insufficient Funds, you only have $" + str(balance) + " avalible.")
            # https://docs.djangoproject.com/en/1.9/topics/forms/#rendering-form-error-messages

        transaction.payee = User.objects.get(id=transaction.payee)  # makes the transaction in the account_view more readable
        Transaction.objects.create(user=transaction.payee, transaction_type='+', ammount=transaction.ammount, payee=transaction.user)

        return super().form_valid(form)
