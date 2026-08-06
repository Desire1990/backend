from rest_framework import serializers
from .models import Supplier, Purchase

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'supplier', 'supplier_name', 'medicine', 'medicine_name',
            'quantity', 'cost_price', 'total_cost', 'date'
        ]

    def get_total_cost(self, obj):
        return float(obj.quantity * obj.cost_price)