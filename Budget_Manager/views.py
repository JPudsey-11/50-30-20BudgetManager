from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm

    if request.method == 'POST':
        if 'add_income' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = Income(
                    user=request.user,
                    source=income_form.cleaned_data['source'],
                    planned_amount=income_form.cleaned_data['planned_amount'],
                    received_amount=income_form.cleaned_data['received_amount'],
                    date=income_form.cleaned_data['date']
                )
                income.save()
                return redirect('dashboard')