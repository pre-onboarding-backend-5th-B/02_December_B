from rest_framework import serializers

from .models import Account


class InvestmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "stock_broker", "number", "total_asset"]


class InvestmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "stock_broker", "number", "total_asset", "investment_principal"]
