from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date
import json
from collections import defaultdict

from .models import Transaction
from .forms import TransactionForm


@login_required
def dashboard(request):
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    transactions = Transaction.objects.filter(user=request.user, date__month=month, date__year=year)

    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expense

    # Category breakdown for pie chart (expenses only)
    category_data = transactions.filter(type='expense').values('category').annotate(total=Sum('amount'))
    pie_labels = [item['category'] for item in category_data]
    pie_values = [float(item['total']) for item in category_data]

    # Monthly bar chart (last 6 months)
    bar_labels = []
    bar_income = []
    bar_expense = []
    for i in range(5, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year - ((today.month - i - 1) // 12)
        month_name = date(y, m, 1).strftime('%b %Y')
        bar_labels.append(month_name)
        inc = Transaction.objects.filter(user=request.user, date__month=m, date__year=y, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        exp = Transaction.objects.filter(user=request.user, date__month=m, date__year=y, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        bar_income.append(float(inc))
        bar_expense.append(float(exp))

    recent_transactions = transactions[:8]

    months = [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    years = list(range(today.year - 3, today.year + 2))

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'recent_transactions': recent_transactions,
        'pie_labels': json.dumps(pie_labels),
        'pie_values': json.dumps(pie_values),
        'bar_labels': json.dumps(bar_labels),
        'bar_income': json.dumps(bar_income),
        'bar_expense': json.dumps(bar_expense),
        'selected_month': month,
        'selected_year': year,
        'months': months,
        'years': years,
        'current_month_name': date(year, month, 1).strftime('%B %Y'),
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def transaction_list(request):
    qs = Transaction.objects.filter(user=request.user)
    type_filter = request.GET.get('type', '')
    category_filter = request.GET.get('category', '')
    currency_filter = request.GET.get('currency', '')
    month_filter = request.GET.get('month', '')
    year_filter = request.GET.get('year', '')

    if type_filter:
        qs = qs.filter(type=type_filter)
    if category_filter:
        qs = qs.filter(category=category_filter)
    if currency_filter:
        qs = qs.filter(currency=currency_filter)
    if month_filter:
        qs = qs.filter(date__month=month_filter)
    if year_filter:
        qs = qs.filter(date__year=year_filter)

    total_income = qs.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = qs.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    from .models import CATEGORY_CHOICES, CURRENCY_CHOICES
    today = date.today()
    months = [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    years = list(range(today.year - 3, today.year + 2))

    context = {
        'transactions': qs,
        'total_income': total_income,
        'total_expense': total_expense,
        'categories': CATEGORY_CHOICES,
        'currencies': CURRENCY_CHOICES,
        'months': months,
        'years': years,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'currency_filter': currency_filter,
        'month_filter': month_filter,
        'year_filter': year_filter,
    }
    return render(request, 'tracker/transaction_list.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard')
    else:
        form = TransactionForm(initial={'date': date.today()})
    return render(request, 'tracker/transaction_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/transaction_form.html', {'form': form, 'action': 'Edit', 'transaction': transaction})


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction_list')
    return render(request, 'tracker/confirm_delete.html', {'transaction': transaction})
