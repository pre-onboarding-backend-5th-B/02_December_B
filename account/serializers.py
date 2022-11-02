from rest_framework import serializers

from .models import Account


class InvestmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "stock_broker", "number", "total_asset"]


class InvestmentDetailSerializer(serializers.ModelSerializer):
    total_return = serializers.SerializerMethodField()
    return_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "name",
            "stock_broker",
            "number",
            "total_asset",
            "investment_principal",
            "total_return",
            "return_percentage",
        ]

    def get_total_return(self, obj):
        res = obj.total_asset - obj.investment_principal
        return res

    def get_return_percentage(self, obj):
        res = (obj.total_asset - obj.investment_principal) / (obj.investment_principal * 100)
        return res
