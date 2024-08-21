from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Income, Expense, User  # Import your custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # Specify your custom user model here
        fields = UserCreationForm.Meta.fields  # Use the same fields as the default form

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'planned_amount', 'received_amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'planned_amount', 'spent_amount']