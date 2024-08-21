from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def dashboard(request):
    # Fetch incomes and expenses
    incomes = Income.objects.filter(user=request.user)
    fun_expenses = Expense.objects.filter(user=request.user, category='Fun')
    fundamentals_expenses = Expense.objects.filter(user=request.user, category='Fundamentals')
    future_you_expenses = Expense.objects.filter(user=request.user, category='Future You')

    # Calculate total income
    total_income = incomes.aggregate(total=Sum('received_amount'))['total'] or 0

    # Calculate planned and spent amounts for each category
    planned_fundamentals = fundamentals_expenses.aggregate(total=Sum('planned_amount'))['total'] or 0
    spent_fundamentals = fundamentals_expenses.aggregate(total=Sum('spent_amount'))['total'] or 0

    planned_fun = fun_expenses.aggregate(total=Sum('planned_amount'))['total'] or 0
    spent_fun = fun_expenses.aggregate(total=Sum('spent_amount'))['total'] or 0

    planned_future_you = future_you_expenses.aggregate(total=Sum('planned_amount'))['total'] or 0
    spent_future_you = future_you_expenses.aggregate(total=Sum('spent_amount'))['total'] or 0

    # Calculate remaining amount
    total_spent = spent_fundamentals + spent_fun + spent_future_you
    remaining_amount = total_income - total_spent

    # Calculate percentages of income spent on each category
    def calculate_percentage(amount):
        return (amount / total_income * 100) if total_income > 0 else 0

    fundamentals_percentage = calculate_percentage(spent_fundamentals)
    fun_percentage = calculate_percentage(spent_fun)
    future_you_percentage = calculate_percentage(spent_future_you)

    # Calculate percentages of planned amounts
    planned_fundamentals_percentage = calculate_percentage(planned_fundamentals)
    planned_fun_percentage = calculate_percentage(planned_fun)
    planned_future_you_percentage = calculate_percentage(planned_future_you)

    # Create the context
    context = {
        'incomes': incomes,
        'fun_expenses': fun_expenses,
        'fundamentals_expenses': fundamentals_expenses,
        'future_you_expenses': future_you_expenses,
        'income_form': IncomeForm(),
        'expense_form': ExpenseForm(),
        'total_income': total_income,
        'planned_fundamentals': planned_fundamentals,
        'spent_fundamentals': spent_fundamentals,
        'planned_fun': planned_fun,
        'spent_fun': spent_fun,
        'planned_future_you': planned_future_you,
        'spent_future_you': spent_future_you,
        'remaining_amount': remaining_amount,
        'fundamentals_percentage': fundamentals_percentage,
        'fun_percentage': fun_percentage,
        'future_you_percentage': future_you_percentage,
        'planned_fundamentals_percentage': planned_fundamentals_percentage,
        'planned_fun_percentage': planned_fun_percentage,
        'planned_future_you_percentage': planned_future_you_percentage,
    }

    return render(request, 'dashboard.html', context)

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

@login_required
def get_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    data = {
        'success': True,
        'income': {
            'source': income.source,
            'planned_amount': str(income.planned_amount),
            'received_amount': str(income.received_amount),
        }
    }
    return JsonResponse(data)

@login_required
def get_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    data = {
        'success': True,
        'expense': {
            'description': expense.description,
            'planned_amount': str(expense.planned_amount),
            'spent_amount': str(expense.spent_amount),
            'category': expense.category,
        }
    }
    return JsonResponse(data)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def guide(request):
    return render(request, 'guide.html')