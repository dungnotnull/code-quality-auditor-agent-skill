# orders/views.py - Django E-Commerce Order Views (INTENTIONALLY FLAWED)

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from payments.services import PaymentService
import logging

logger = logging.getLogger(__name__)


class OrderListView(APIView):
    """List all orders - FLAW: No authentication required, any user can see all orders."""
    # FLAW: Missing authentication_classes and permission_classes

    def get(self, request):
        orders = Order.objects.all()  # FLAW: Returns ALL orders, not filtered by user (IDOR)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    """Get a single order - FLAW: No authorization check (IDOR)."""

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)  # FLAW: Any authenticated user can access any order
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderCreateView(APIView):
    """Create a new order - FLAW: No idempotency key, double-submit creates duplicate orders."""

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # FLAW: Payment is triggered synchronously with no idempotency protection
            payment_service = PaymentService()
            try:
                payment_service.charge(serializer.instance)
            except Exception:  # FLAW: Bare except - silent payment failure
                pass  # FLAW: Order created but payment failed silently
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelView(APIView):
    """Cancel an order - FLAW: No state transition validation."""

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        # FLAW: Can cancel already cancelled/shipped/delivered orders
        order.status = 'cancelled'
        order.save()
        # FLAW: No refund triggered for paid orders
        return Response({'status': 'cancelled'})


@api_view(['POST'])
@permission_classes([AllowAny])  # FLAW: AllowAny on order creation
def place_order(request):
    """Direct function-based view for order placement - FLAW: No auth, no validation."""
    data = request.data
    order = Order.objects.create(
        user=request.user,  # FLAW: Will crash if user not authenticated (AllowAny)
        total_amount=data.get('total_amount', 0),  # FLAW: User-provided total, no server-side calc
        shipping_address=data.get('shipping_address', ''),
        status='pending',
    )
    # FLAW: No transaction atomic block - race condition on order + items creation
    for item_data in data.get('items', []):
        OrderItem.objects.create(
            order=order,
            product_name=item_data.get('name', ''),
            product_price=item_data.get('price', 0),
            quantity=item_data.get('quantity', 1),
            subtotal=item_data.get('price', 0) * item_data.get('quantity', 1),
        )

    # FLAW: God method doing too much - order creation + payment + notification
    payment_service = PaymentService()
    try:
        charge = payment_service.charge(order)
    except:  # FLAW: Bare except with no logging
        pass

    # FLAW: No notification service call - incomplete business flow

    return Response({'order_id': order.id}, status=status.HTTP_201_CREATED)
