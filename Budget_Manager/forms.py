from django import forms

class IncomeForm(forms.Form):
    source = forms.CharField()
    planned_amount = forms.DecimalField()
    received_amount = forms.DecimalField()
    date = forms.DateField()

