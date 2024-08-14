from django.shortcuts import render, redirect, get_object_or_404
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
            income_id = request.POST.get('income_id')
            if income_id:
                income = get_object_or_404(Income, id=income_id, user=request.user)
            else:
                income = Income(user=request.user)

            income_form = IncomeForm(request.POST, instance=income)
            if income_form.is_valid():
                income_form.save()
                return redirect('dashboard')

        elif 'expense_submit' in request.POST:
            expense_id = request.POST.get('expense_id')
            if expense_id:
                expense = get_object_or_404(Expense, id=expense_id, user=request.user)
            else:
                expense = Expense(user=request.user)

            expense_form = ExpenseForm(request.POST, instance=expense)
            if expense_form.is_valid():
                expense.category = request.POST.get('category')
                expense_form.save()
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
def get_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    return JsonResponse({
        'success': True,
        'income': {
            'id': income.id,
            'source': income.source,
            'planned_amount': str(income.planned_amount),
            'received_amount': str(income.received_amount),
        }
    })

@login_required
def get_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    return JsonResponse({
        'success': True,
        'expense': {
            'id': expense.id,
            'description': expense.description,
            'planned_amount': str(expense.planned_amount),
            'spent_amount': str(expense.spent_amount),
            'category': expense.category,
        }
    })

@login_required
def delete_income(request, income_id):
    try:
        income = Income.objects.get(id=income_id, user=request.user)
        income.delete()
        return JsonResponse({'success': True})
    except Income.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Income not found.'})

@login_required
def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
        expense.delete()
        return JsonResponse({'success': True})
    except Expense.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Expense not found.'})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
