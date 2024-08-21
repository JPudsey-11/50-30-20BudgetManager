from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Income, Expense, User

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'planned_amount', 'received_amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'planned_amount', 'spent_amount']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User  # Ensure this references your custom user model
        fields = ('username', 'password1', 'password2')