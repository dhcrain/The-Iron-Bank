from django import forms
from bank_app.models import Transaction

class TransferFrom(models.ModelForm)

    payee_choices(auth.User, "auth.User")

    class Meta:
        model = Transaction
        fields = ['ammount', 'payee']
        # payee = forms.TypedChoiceField(label='Transfer funds to Account number: ')
        payee = forms.TypedChoiceField(choices=payee_choices, coerce=int)
