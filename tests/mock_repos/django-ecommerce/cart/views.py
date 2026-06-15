# cart/views.py - Cart Views (INTENTIONALLY FLAWED)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view(['GET'])
@permission_classes([AllowAny])
def cart_view(request):
    """Get cart contents - FLAW: Uses session without auth, no session validation."""
    cart = request.session.get('cart', {})
    return Response(cart)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart(request):
    """Add item to cart - FLAW: No quantity validation, no product existence check."""
    cart = request.session.get('cart', {})
    product_id = str(request.data.get('product_id'))
    quantity = request.data.get('quantity', 1)  # FLAW: No validation - negative qty allowed

    if product_id in cart:
        cart[product_id] += quantity  # FLAW: Can go negative, no upper bound
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    return Response(cart)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_cart_item(request, product_id):
    """Update cart item quantity - FLAW: No validation."""
    cart = request.session.get('cart', {})
    quantity = request.data.get('quantity')  # FLAW: No type check, no range check
    cart[str(product_id)] = quantity  # FLAW: Can set any value including negative
    request.session['cart'] = cart
    return Response(cart)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_cart(request):
    """Clear entire cart - FLAW: No confirmation, no CSRF protection on DELETE."""
    request.session['cart'] = {}
    return Response({'status': 'cleared'})
