from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Prescription
from .serializers import PrescriptionSerializer
from apps.accounts.permissions import IsAdminOrReadOnly, IsAdminUser
from rest_framework.decorators import action

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'verify']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAdminOrReadOnly]  # list & create allowed for all authenticated
        return super().get_permissions()

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient_name', 'doctor_name']
    ordering = ['-created_at']

    # Custom action for verifying prescription
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        prescription = self.get_object()
        prescription.verified = True
        prescription.save()
        return Response({'status': 'verified'})