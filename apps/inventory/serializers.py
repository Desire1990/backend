from rest_framework import serializers
from .models import Category, Medicine

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    low_stock = serializers.BooleanField(source='is_low_stock', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    profit_margin = serializers.SerializerMethodField(read_only=True)
    profit_per_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'category', 'category_name', 'brand', 'batch_number',
            'expiry_date', 'cost_price', 'selling_price', 'quantity', 'reorder_level',
            'low_stock', 'profit_margin', 'profit_per_unit', 'created_at', 'updated_at'
        ]

    def get_profit_margin(self, obj):
        return float(obj.profit_margin)

    def get_profit_per_unit(self, obj):
        return float(obj.profit_per_unit)