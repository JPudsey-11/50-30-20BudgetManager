from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_income/<int:income_id>/', views.delete_income, name='delete_income'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('get_income/<int:income_id>/', views.get_income, name='get_income'),
    path('get_expense/<int:expense_id>/', views.get_expense, name='get_expense'),
    path('signup/', views.SignUpView.as_view(), name='signup'),  # Sign-Up URL
    path('', views.dashboard, name='home'),
]