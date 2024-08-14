from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    fun_expenses = Expense.objects.filter(user=request.user, category='Fun')
    fundamentals_expenses = Expense.objects.filter(user=request.user, category='Fundamentals')
    future_you_expenses = Expense.objects.filter(user=request.user, category='Future You')

    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = Income(
                    user=request.user,
                    source=income_form.cleaned_data['source'],
                    planned_amount=income_form.cleaned_data['planned_amount'],
                    received_amount=income_form.cleaned_data['received_amount'],
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
                )
                expense.save()
                return redirect('dashboard')
    else:
        income_form = IncomeForm()
        expense_form = ExpenseForm()

    context = {
        'incomes': incomes,
        'fun_expenses': fun_expenses,
        'fundamentals_expenses': fundamentals_expenses,
        'future_you_expenses': future_you_expenses,
        'income_form': income_form,
        'expense_form': expense_form,
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        print("Received POST request for income:", request.POST)
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            print("Income saved successfully:", income)
            return redirect('dashboard')
        else:
            print("Income form is not valid:", form.errors)
    else:
        form = IncomeForm()
        print("Rendering form for GET request (add_income)")
    return render(request, 'add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        print("Received POST request for expense:", request.POST)
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            category = request.POST.get('category')  # Extract the category from POST data
            if category:
                expense.category = category
                print(f"Setting category: {category}")  # Log the category being set
            else:
                print("No category found in the POST data")  # Log if category is missing
            expense.save()
            print("Expense saved successfully:", expense)  # Log after saving the expense
            return redirect('dashboard')
        else:
            print("Expense form is not valid:", form.errors)  # Log if the form is not valid
    else:
        form = ExpenseForm()
        print("Rendering form for GET request (add_expense)")  # Log when the form is being rendered on GET request
    return render(request, 'add_expense.html', {'form': form})

@login_required
def delete_income(request, income_id):
    try:
        print(f"Attempting to delete income with ID: {income_id}")
        income = Income.objects.get(id=income_id, user=request.user)
        income.delete()
        print("Income deleted successfully")
        return JsonResponse({'success': True})
    except Income.DoesNotExist:
        print("Income not found")
        return JsonResponse({'success': False, 'error': 'Income not found.'})

@login_required
def delete_expense(request, expense_id):
    try:
        print(f"Attempting to delete expense with ID: {expense_id}")
        expense = Expense.objects.get(id=expense_id, user=request.user)
        expense.delete()
        print("Expense deleted successfully")
        return JsonResponse({'success': True})
    except Expense.DoesNotExist:
        print("Expense not found")
        return JsonResponse({'success': False, 'error': 'Expense not found.'})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
