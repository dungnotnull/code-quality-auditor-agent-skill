# shop/urls.py - Django E-Commerce URL Configuration

from django.contrib import admin
from django.urls import path, include
from orders.views import OrderListView  # FLAW: importing view directly for unauthenticated access

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/orders/', OrderListView.as_view()),  # FLAW: No authentication required
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/cart/', include('cart.urls')),
]
