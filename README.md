# Flo — Expense Tracker

A Django-based expense tracker with income/expense logging, multi-currency support, and charts.

## Features
- User registration & login
- Add / Edit / Delete transactions
- Income & Expense categorization
- Multi-currency: INR, USD, EUR, GBP, JPY, AUD
- Dashboard with Pie & Bar charts (Chart.js)
- Filter by type, category, currency, month, year
- Clean dark UI

## Setup Instructions

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### 5. Start the server
```bash
python manage.py runserver
```

### 6. Open in browser
```
http://127.0.0.1:8000/
```

## Project Structure
```
expense_tracker/
├── manage.py
├── requirements.txt
├── expense_tracker/        # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # Auth app
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/
│       ├── login.html
│       └── register.html
├── tracker/                # Core app
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/tracker/
│       ├── dashboard.html
│       ├── transaction_list.html
│       ├── transaction_form.html
│       └── confirm_delete.html
└── templates/
    └── base.html
```

## Models
- **Transaction**: title, amount, currency, type (income/expense), category, date, note

## URLs
| URL | View |
|-----|------|
| `/` | Dashboard |
| `/transactions/` | All transactions with filters |
| `/transactions/add/` | Add new transaction |
| `/transactions/<id>/edit/` | Edit transaction |
| `/transactions/<id>/delete/` | Delete transaction |
| `/accounts/login/` | Login |
| `/accounts/register/` | Register |
| `/accounts/logout/` | Logout |
