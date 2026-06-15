# products/views.py - Django E-Commerce Product Views

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


@api_view(['GET'])
def product_list(request):
    """List all products - FLAW: N+1 query problem with categories."""
    products = Product.objects.all()  # FLAW: No select_related/prefetch_related for category FK
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def product_search(request):
    """Search products - FLAW: Raw SQL with unsanitized user input (SQL injection)."""
    query = request.query_params.get('q', '')
    from django.db import connection
    cursor = connection.cursor()
    # FLAW: SQL injection - user input directly in query string
    cursor.execute(f"SELECT * FROM products_product WHERE name LIKE '%{query}%'")
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            'id': row[0],
            'name': row[1],
            'price': row[2],
        })
    return Response(results)
