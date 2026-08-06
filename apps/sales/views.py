from rest_framework import viewsets, filters
from .models import Sale
from .serializers import SaleSerializer
from apps.accounts.permissions import IsAdminOrReadOnly

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.prefetch_related('items__medicine').all()
    serializer_class = SaleSerializer
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer_name', 'items__medicine__name']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Date range filter
        start = self.request.query_params.get('start_date')
        end = self.request.query_params.get('end_date')
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        
        # Role-based filtering
        user_id = self.request.query_params.get('user')
        if user_id:
            qs = qs.filter(user_id=user_id)
        elif not self.request.user.is_staff and self.request.user.role != 'admin':
            qs = qs.filter(user=self.request.user)
        
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)