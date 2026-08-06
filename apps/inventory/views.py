from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Medicine
from .serializers import CategorySerializer, MedicineSerializer
from .filters import MedicineFilter
from apps.accounts.permissions import IsAdminOrReadOnly, IsAdminUser

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.select_related('category').all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicineFilter
    search_fields = ['name', 'brand', 'batch_number']
    ordering_fields = ['name', 'expiry_date', 'cost_price', 'selling_price', 'quantity','created_at']
    ordering = ['name']

    @action(methods=['post'], detail=False, url_path='bulk', permission_classes=[IsAdminUser])
    @transaction.atomic
    def bulk_create(self, request):
        serializer = MedicineSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        serializer.save()