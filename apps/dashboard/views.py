from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta

from apps.inventory.models import Medicine
from apps.inventory.serializers import MedicineSerializer
from apps.sales.models import Sale

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        last_7_days = today - timedelta(days=6)
        start_of_month = today.replace(day=1)

        # Medicine stats
        total_medicines = Medicine.objects.count()
        low_stock = Medicine.objects.filter(quantity__lte=F('reorder_level'))
        low_stock_serializer = MedicineSerializer(low_stock, many=True)

        # Inventory value
        total_inventory_cost = Medicine.objects.aggregate(
            total=Sum(F('quantity') * F('cost_price'))
        )['total'] or 0

        total_inventory_value = Medicine.objects.aggregate(
            total=Sum(F('quantity') * F('selling_price'))
        )['total'] or 0

        potential_profit = total_inventory_value - total_inventory_cost

        # Sales stats
        today_sales = Sale.objects.filter(created_at__date=today).aggregate(
            total=Sum('total')
        )['total'] or 0

        weekly_sales = Sale.objects.filter(created_at__date__gte=last_7_days).aggregate(
            total=Sum('total')
        )['total'] or 0

        monthly_sales = Sale.objects.filter(created_at__date__gte=start_of_month).aggregate(
            total=Sum('total')
        )['total'] or 0

        # Expiring soon
        expiring_soon = Medicine.objects.filter(
            expiry_date__lte=today + timedelta(days=30),
            expiry_date__gte=today
        ).count()

        return Response({
            'total_medicines': total_medicines,
            'low_stock': low_stock_serializer.data,
            'total_inventory_cost': total_inventory_cost,
            'total_inventory_value': total_inventory_value,
            'potential_profit': potential_profit,
            'today_sales': today_sales,
            'weekly_sales': weekly_sales,
            'monthly_sales': monthly_sales,
            'expiring_soon': expiring_soon,
        })