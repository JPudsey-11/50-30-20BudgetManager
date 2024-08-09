from django.shortcuts import render, redirect
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'income_submit' in request.POST:
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
        elif 'expense_submit' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = Expense(
                    user=request.user,
                    description=expense_form.cleaned_data['description'],
                    planned_amount=expense_form.cleaned_data['planned_amount'],
                    spent_amount=expense_form.cleaned_data['spent_amount'],
                    category=expense_form.cleaned_data['category'],
                    date=expense_form.cleaned_data['date']
                )
                expense.save()
                return redirect('dashboard')
    else:
        income_form = IncomeForm()
        expense_form = ExpenseForm()

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'income_form': income_form,
        'expense_form': expense_form,
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})
