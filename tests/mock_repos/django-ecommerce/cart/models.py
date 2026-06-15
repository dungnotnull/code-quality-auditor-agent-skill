# cart/models.py

from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        """Calculate cart total - FLAW: N+1 query."""
        total = 0
        for item in self.items.all():  # FLAW: Queries each item's product individually
            total += item.product.price * item.quantity
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # OK: PositiveIntegerField

    class Meta:
        # FLAW: Missing unique constraint on (cart, product) - allows duplicate products
        pass
