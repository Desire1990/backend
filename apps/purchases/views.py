from rest_framework import viewsets, filters
from .models import Supplier, Purchase
from .serializers import SupplierSerializer, PurchaseSerializer
from apps.accounts.permissions import IsAdminOrReadOnly

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'email']

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.select_related('supplier', 'medicine').all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medicine__name', 'supplier__name']
    ordering_fields = ['date', 'cost_price']
    ordering = ['-date']