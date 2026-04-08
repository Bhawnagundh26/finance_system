from transactions.models import Transaction
from collections import defaultdict
from decimal import Decimal


def get_summary(user, role):
    if role in ('admin', 'analyst'):
        qs = Transaction.objects.all()
    else:
        qs = Transaction.objects.filter(owner=user)

    transactions = list(qs)

    total_income  = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance       = total_income - total_expense

    category_totals = defaultdict(Decimal)
    for t in transactions:
        category_totals[t.category] += t.amount

    monthly = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})
    for t in transactions:
        key = t.date.strftime('%Y-%m')
        monthly[key][t.type] += t.amount

    recent = sorted(transactions, key=lambda t: t.date, reverse=True)[:5]
    recent_list = [
        {
            'id': t.id,
            'amount': str(t.amount),
            'type': t.type,
            'category': t.category,
            'date': str(t.date),
            'notes': t.notes,
        }
        for t in recent
    ]

    return {
        'total_income':       str(round(total_income, 2)),
        'total_expense':      str(round(total_expense, 2)),
        'balance':            str(round(balance, 2)),
        'category_breakdown': {k: str(v) for k, v in category_totals.items()},
        'monthly_totals':     {k: {ik: str(iv) for ik, iv in v.items()} for k, v in monthly.items()},
        'recent_transactions': recent_list,
    }