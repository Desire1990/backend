from django.db import models
from apps.inventory.models import Medicine

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Purchase price per unit")
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            # Increase stock
            self.medicine.quantity += self.quantity
            # Update medicine's cost price to latest purchase price
            self.medicine.cost_price = self.cost_price
            self.medicine.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Reverse stock when deleting a purchase
        self.medicine.quantity -= self.quantity
        self.medicine.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} units from {self.supplier.name}"