"""iron_bank_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from bank_app.views import IndexView, AccountView, TransactionDetailView, TransferView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url('^register/', CreateView.as_view(template_name='register.html', form_class=UserCreationForm, success_url='/login'), name='register_view'),
    url(r'^account/$', AccountView.as_view(), name='account_view'),
    url(r'^account/transfer$', TransferView.as_view(), name='transfer_view'),
    url(r'^account/detail/(?P<pk>\d+)', TransactionDetailView.as_view(), name='detail_view'),
]
