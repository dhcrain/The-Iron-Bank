from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from bank_app.models import Transaction


# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

class AccountView(ListView):
    model = Transaction
