from django import forms

class IncomeForm(forms.Form):
    source = forms.CharField()
    planned_amount = forms.DecimalField()
    received_amount = forms.DecimalField()
    date = forms.DateField()

class ExpenseForm(forms.Form):
    description = forms.CharField()
    planned_amount = forms.DecimalField()
    spent_amount = forms.DecimalField()
    category = forms.ChoiceField(choices=[
        ('Fundamentals', 'Fundamentals'),
        ('Fun', 'Fun'),
        ('Future You', 'Future You'),
    ])
    date = forms.DateField()