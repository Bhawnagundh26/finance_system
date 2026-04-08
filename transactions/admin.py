from django.contrib import admin
from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ['id', 'owner', 'type', 'amount', 'category', 'date']
    list_filter   = ['type', 'category', 'date']
    search_fields = ['category', 'notes', 'owner__username']