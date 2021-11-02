from rest_framework import serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class InvoiceItemsSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = InvoiceItem
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ("quantity", "item")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Invoice
        fields = ("id", "customer", "timestamp")