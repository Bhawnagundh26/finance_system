from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer, TransactionUpdateSerializer
from transactions.permissions import IsAdmin, IsAnalystOrAdmin, IsAnyRole
from transactions.services import get_summary


class TransactionListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAnyRole()]

    def get(self, request):
        role = request.user.role
        if role in ('admin', 'analyst'):
            qs = Transaction.objects.all()
        else:
            qs = Transaction.objects.filter(owner=request.user)

        tx_type    = request.query_params.get('type')
        category   = request.query_params.get('category')
        start_date = request.query_params.get('start_date')
        end_date   = request.query_params.get('end_date')

        if tx_type:
            qs = qs.filter(type=tx_type)
        if category:
            qs = qs.filter(category__icontains=category)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        page      = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start     = (page - 1) * page_size
        end       = start + page_size
        total     = qs.count()

        return Response({
            'total':     total,
            'page':      page,
            'page_size': page_size,
            'results':   TransactionSerializer(qs[start:end], many=True).data
        })

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):

    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAdmin()]
        return [IsAnyRole()]

    def get_object(self, pk, user, role):
        try:
            tx = Transaction.objects.get(pk=pk)
            if role not in ('admin', 'analyst') and tx.owner != user:
                return None, 'forbidden'
            return tx, None
        except Transaction.DoesNotExist:
            return None, 'not_found'

    def get(self, request, pk):
        tx, err = self.get_object(pk, request.user, request.user.role)
        if err == 'not_found':
            return Response({'error': 'Transaction not found'}, status=404)
        if err == 'forbidden':
            return Response({'error': 'Access denied'}, status=403)
        return Response(TransactionSerializer(tx).data)

    def patch(self, request, pk):
        tx, err = self.get_object(pk, request.user, request.user.role)
        if err == 'not_found':
            return Response({'error': 'Transaction not found'}, status=404)
        if err == 'forbidden':
            return Response({'error': 'Access denied'}, status=403)
        serializer = TransactionUpdateSerializer(tx, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(TransactionSerializer(tx).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        tx, err = self.get_object(pk, request.user, request.user.role)
        if err == 'not_found':
            return Response({'error': 'Transaction not found'}, status=404)
        if err == 'forbidden':
            return Response({'error': 'Access denied'}, status=403)
        tx.delete()
        return Response({'message': 'Transaction deleted successfully'}, status=200)


class SummaryView(APIView):
    permission_classes = [IsAnalystOrAdmin]

    def get(self, request):
        return Response(get_summary(request.user, request.user.role))