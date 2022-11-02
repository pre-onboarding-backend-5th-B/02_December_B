from rest_framework import serializers

from .models import Account


class InvestmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "number", "investment_principal", "total_asset"]
