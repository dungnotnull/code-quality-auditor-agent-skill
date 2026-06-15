# orders/models.py - Django E-Commerce Order Models

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # FLAW: No validation on positive amount
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.TextField()

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)  # FLAW: No MinValueValidator for quantity
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # FLAW: Subtotal calculation can drift from actual price * quantity
        # if someone sets subtotal directly without recalculation
        self.subtotal = self.product_price * self.quantity  # FLAW: Decimal * Int precision issue
        super().save(*args, **kwargs)


class PaymentRecord(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    stripe_charge_id = models.CharField(max_length=255, blank=True)  # FLAW: blank=True allows no charge tracking
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    refunded = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # FLAW: No constraint that refund_amount <= amount
