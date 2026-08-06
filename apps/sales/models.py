from django.db import models
from apps.accounts.models import User
from apps.inventory.models import Medicine

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales')
    customer_name = models.CharField(max_length=100, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.created_at.date()}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} x{self.quantity}"