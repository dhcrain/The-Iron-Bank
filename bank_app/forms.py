from django import forms
from bank_app.models import Transaction
from django.contrib.auth.models import User



class TransferForm(forms.ModelForm):

    payee_choices = (User, "User")
    payee = forms.TypedChoiceField(choices=payee_choices, coerce=int)
    # ammount = form.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Transaction
        fields = ['payee', 'ammount']


        labels = {
                    'payee': ('Transfer funds to this account number:'),
                    'ammount': ('Transfer this ammount:'),
                }
        error_messages = {'payee': {'user': ("Not a valid account number"),},
            }

        def clean_payee(self):
            if payee not in auth.User:
                pass
