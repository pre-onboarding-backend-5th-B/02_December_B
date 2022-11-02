from django.core.validators import MinValueValidator
from rest_framework import serializers

from transfer.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', 'account', 'price', 'status']
        extra_kwargs = {
            'price': {
                'validators': [MinValueValidator(0)],
                'required': True,
                'allow_null': False
            },
            'status': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        return Transfer.objects.create(status=Transfer.PENDING, **validated_data)


class TransferDetailSerializer(serializers.ModelSerializer):
    signature = serializers.CharField(write_only=True)

    class Meta:
        model = Transfer
        fields = ['signature', 'status']
        extra_kwargs = {
            'signature': {'write_only': True, },
            'status': {'read_only': True, }
        }
