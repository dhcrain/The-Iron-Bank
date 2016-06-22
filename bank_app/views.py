import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from bank_app.models import Transaction
from django.http import request, HttpResponse
from django.db.models.base import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy


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


class AccountView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'bank_app/transaction_list.html'
    fields = ['transaction_type', 'ammount', 'payee']
    success_url = reverse_lazy('account_view')

    def get_context_data(self, **kwargs):
        get_balance(self)
        context = super().get_context_data(**kwargs)
        context["balance"] = self.acct_balance
        thirty_days_ago = datetime.datetime.now() + datetime.timedelta(days=-30)
        context['transactions'] = Transaction.objects.filter(user=self.request.user).filter(date__gt=thirty_days_ago)
        return context


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
                form.add_error('ammount', "Insufficient Funds, you only have $" + str(balance) + " avalible.")
                return self.form_invalid(form)
        return super().form_valid(form)

class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransferView(CreateView):
    model = Transaction
    fields = ['payee', 'ammount']
    # form_class = TransferForm
    template_name = 'bank_app/transfer.html'
    success_url = reverse_lazy('account_view')


    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.transaction_type='-'    # take money out of users account
        balance = get_balance(self)

        if (balance - transaction.ammount) <= 0:
            form.add_error('ammount', "Insufficient Funds, you only have $" + str(balance) + " avalible.")
            return self.form_invalid(form)

        try:
            User.objects.get(id=transaction.payee)      # this is what it is trying, not idle like you thought when you deleted it and broke everything
            if int(self.request.user.id) == int(transaction.payee):
                form.add_error('payee', "Why are you trying to trasfer money to yourself?")
                return self.form_invalid(form)
        except ObjectDoesNotExist:
            form.add_error('payee', "That account does not exist")
            return self.form_invalid(form)

        transaction.payee = User.objects.get(id=transaction.payee)  # makes the transaction in the account_view more readable
        Transaction.objects.create(user=transaction.payee, transaction_type='+', ammount=transaction.ammount, payee=transaction.user)

        return super().form_valid(form)
