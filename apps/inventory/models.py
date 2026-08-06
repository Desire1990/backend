from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='medicines')
    brand = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    
    # Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Purchase price from supplier")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price sold to customers")
    
    # Stock
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price and self.cost_price > 0:
            return round(((self.selling_price - self.cost_price) / self.cost_price) * 100, 2)
        return 0

    @property
    def profit_per_unit(self):
        """Calculate profit per unit"""
        return self.selling_price - self.cost_price

    def __str__(self):
        return f"{self.name} ({self.brand})"