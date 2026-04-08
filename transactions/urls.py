from django.urls import path
from transactions.views import TransactionListCreateView, TransactionDetailView, SummaryView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('summary/', SummaryView.as_view(), name='summary'),
]