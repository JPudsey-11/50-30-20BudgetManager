from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # Ensuring we're using the correct manager

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)  # Automatically set the current date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source}: {self.planned_amount} / {self.received_amount}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Fundamentals', 'Fundamentals'),
        ('Fun', 'Fun'),
        ('Future You', 'Future You'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)  # Automatically set the current date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}: {self.planned_amount} / {self.spent_amount}"