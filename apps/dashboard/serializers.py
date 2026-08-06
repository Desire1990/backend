from rest_framework import serializers
from apps.inventory.serializers import MedicineSerializer

class DashboardSerializer(serializers.Serializer):
    total_medicines = serializers.IntegerField()
    low_stock = MedicineSerializer(many=True)
    today_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekly_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    expiring_soon = serializers.IntegerField()