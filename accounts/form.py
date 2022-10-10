from django import forms
from  accounts.models import *


class Update_form_user(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = '__all__'