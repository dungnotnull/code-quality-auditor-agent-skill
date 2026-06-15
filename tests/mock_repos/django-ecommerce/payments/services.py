# payments/services.py - Payment Service (INTENTIONALLY FLAWED GOD CLASS)

import stripe
import os
import logging

logger = logging.getLogger(__name__)

# FLAW: Hardcoded Stripe key (also in settings.py)
stripe.api_key = 'FAKE_STRIPE_TEST_KEY_FOR_AUDIT_DEMO_ONLY'


class PaymentService:
    """God class handling payments, refunds, notifications, and receipt generation.
    FLAW: Violates SRP - should be split into PaymentService, RefundService,
    NotificationService, and ReceiptService."""

    def charge(self, order):
        """Charge the customer's card.
        FLAW: No idempotency key - double-charge risk on retry.
        FLAW: No authorization verification before charge."""
        try:
            charge = stripe.Charge.create(
                amount=int(order.total_amount * 100),  # FLAW: Float multiplication for money
                currency='usd',
                source='tok_visa',  # FLAW: Hardcoded test token
                metadata={'order_id': order.id},
            )
            return charge
        except stripe.error.StripeError as e:
            # FLAW: Only catches StripeError, not ConnectionError, Timeout, etc.
            logger.error(f"Payment failed for order {order.id}: {e}")
            # FLAW: Re-raises, but caller has bare except that swallows it
            raise
        except:  # FLAW: Bare except clause
            pass  # FLAW: Silent failure

    def refund(self, order, amount=None):
        """Process a refund.
        FLAW: No authorization check - any caller can trigger refund.
        FLAW: No idempotency key on refund."""
        refund_amount = amount or order.total_amount
        # FLAW: No check that refund_amount <= original charge amount
        # FLAW: No check that order has a successful payment
        try:
            if order.payment and order.payment.stripe_charge_id:
                refund = stripe.Refund.create(
                    charge=order.payment.stripe_charge_id,
                    amount=int(refund_amount * 100),  # FLAW: Float math for money
                )
                order.payment.refunded = True
                order.payment.refund_amount = refund_amount
                order.payment.save()
                self._send_refund_notification(order)  # FLAW: Tight coupling to notification
                return refund
        except Exception as e:  # FLAW: Broad exception catch
            logger.error(f"Refund failed: {e}")
            # FLAW: Returns None silently on failure - caller can't distinguish success vs failure
            return None

    def _send_refund_notification(self, order):
        """Send refund notification - FLAW: Should be in separate NotificationService."""
        # FLAW: Hardcoded email template, no i18n
        subject = f"Refund processed for Order #{order.id}"
        body = f"Your refund of  has been processed."
        # FLAW: No actual email sending implementation
        pass

    def generate_receipt(self, order):
        """Generate PDF receipt - FLAW: Should be in ReceiptService."""
        # FLAW: No receipt template, no PDF generation
        # FLAW: Receipt doesn't include tax information
        receipt_data = {
            'order_id': order.id,
            'amount': order.total_amount,
            'date': str(order.created_at),
        }
        return receipt_data

    def get_payment_history(self, user):
        """Get payment history for a user.
        FLAW: No pagination - will load all records for a user.
        FLAW: No caching - hits DB every time."""
        from orders.models import Order
        orders = Order.objects.filter(user=user)  # FLAW: N+1 - no select_related on payment
        history = []
        for order in orders:
            if hasattr(order, 'payment'):
                history.append({
                    'order_id': order.id,
                    'amount': order.total_amount,
                    'status': order.payment.refunded and 'refunded' or 'completed',
                })
        return history
