# orders/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'created_at', 'updated_at', 'shipping_address', 'items']
        read_only_fields = ['created_at', 'updated_at']  # FLAW: 'status' should be read_only for non-admin
