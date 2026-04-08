from rest_framework import serializers
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'date', 'notes', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_category(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category cannot be empty.")
        return value


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'category', 'date', 'notes']
        extra_kwargs = {
            'amount':   {'required': False},
            'type':     {'required': False},
            'category': {'required': False},
            'date':     {'required': False},
            'notes':    {'required': False},
        }