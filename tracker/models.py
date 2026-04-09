from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


CURRENCY_CHOICES = [
    ('INR', '₹ INR'),
    ('USD', '$ USD'),
    ('EUR', '€ EUR'),
    ('GBP', '£ GBP'),
    ('JPY', '¥ JPY'),
    ('AUD', 'A$ AUD'),
]

CATEGORY_CHOICES = [
    ('Food & Dining', 'Food & Dining'),
    ('Transport', 'Transport'),
    ('Shopping', 'Shopping'),
    ('Entertainment', 'Entertainment'),
    ('Health & Medical', 'Health & Medical'),
    ('Utilities', 'Utilities'),
    ('Rent & Housing', 'Rent & Housing'),
    ('Education', 'Education'),
    ('Travel', 'Travel'),
    ('Salary', 'Salary'),
    ('Freelance', 'Freelance'),
    ('Investment', 'Investment'),
    ('Gift', 'Gift'),
    ('Other', 'Other'),
]

TYPE_CHOICES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='INR')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.amount} {self.currency}"

    def currency_symbol(self):
        symbols = {'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'AUD': 'A$'}
        return symbols.get(self.currency, self.currency)
