import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_system.settings')
django.setup()

from users.models import CustomUser
from transactions.models import Transaction
from datetime import date

print("Seeding data...")

admin_user, _ = CustomUser.objects.get_or_create(username='admin', defaults={'email': 'admin@finance.com', 'role': 'admin'})
admin_user.set_password('admin123')
admin_user.save()

analyst_user, _ = CustomUser.objects.get_or_create(username='analyst', defaults={'email': 'analyst@finance.com', 'role': 'analyst'})
analyst_user.set_password('analyst123')
analyst_user.save()

viewer_user, _ = CustomUser.objects.get_or_create(username='viewer', defaults={'email': 'viewer@finance.com', 'role': 'viewer'})
viewer_user.set_password('viewer123')
viewer_user.save()

sample_transactions = [
    {'amount': 5000, 'type': 'income',  'category': 'Salary',    'date': date(2024, 1, 1),  'notes': 'Jan salary'},
    {'amount': 200,  'type': 'expense', 'category': 'Food',      'date': date(2024, 1, 5),  'notes': 'Groceries'},
    {'amount': 1500, 'type': 'income',  'category': 'Freelance', 'date': date(2024, 2, 10), 'notes': 'Project payment'},
    {'amount': 100,  'type': 'expense', 'category': 'Transport', 'date': date(2024, 2, 15), 'notes': 'Fuel'},
    {'amount': 3000, 'type': 'income',  'category': 'Salary',    'date': date(2024, 3, 1),  'notes': 'Mar salary'},
    {'amount': 500,  'type': 'expense', 'category': 'Utilities', 'date': date(2024, 3, 20), 'notes': 'Electricity'},
]

for t in sample_transactions:
    Transaction.objects.get_or_create(
        owner=admin_user, amount=t['amount'],
        type=t['type'], category=t['category'],
        date=t['date'], defaults={'notes': t['notes']}
    )

print("Done!")
print("  admin   / admin123")
print("  analyst / analyst123")
print("  viewer  / viewer123")