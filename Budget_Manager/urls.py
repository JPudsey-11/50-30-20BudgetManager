from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing-page'),  # Set landing page as the home page
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Income paths
    path('delete_income/<int:income_id>/', views.delete_income, name='delete_income'),
    path('get_income/<int:income_id>/', views.get_income, name='get_income'),
    
    # Expense paths
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('get_expense/<int:expense_id>/', views.get_expense, name='get_expense'),
    
    # Authentication paths
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('guide/', views.guide, name='guide'),
]