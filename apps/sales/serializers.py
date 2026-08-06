from rest_framework import serializers
from .models import Sale, SaleItem
from apps.inventory.models import Medicine
from django.db import transaction

class SaleItemSerializer(serializers.ModelSerializer):
    medicine_id = serializers.IntegerField(write_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    batch_number = serializers.CharField(source='medicine.batch_number', read_only=True)
    expiry_date = serializers.CharField(source='medicine.expiry_date', read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'medicine_id', 'medicine_name', 'quantity', 'price', 'batch_number','expiry_date']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'user', 'user_name', 'customer_name', 'total', 'created_at', 'items']
        read_only_fields = ['user', 'total']

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        
        # Compute total
        total = sum(item['price'] * item['quantity'] for item in items_data)
        validated_data['total'] = total

        sale = Sale.objects.create(**validated_data)

        for item_data in items_data:
            medicine_id = item_data.pop('medicine_id')
            medicine = Medicine.objects.get(pk=medicine_id)
            
            if medicine.quantity < item_data['quantity']:
                raise serializers.ValidationError(
                    f"Insufficient stock for {medicine.name}. Available: {medicine.quantity}"
                )
            
            # Deduct stock
            medicine.quantity -= item_data['quantity']
            medicine.save()
            
            SaleItem.objects.create(sale=sale, medicine=medicine, **item_data)

        return sale