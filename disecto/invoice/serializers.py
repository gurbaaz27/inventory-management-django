from rest_framework import serializers
from .models import Item, InvoiceItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ("quantity", "item")