from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Import all models
from apps.accounts.models import User
from apps.inventory.models import Category, Medicine
from apps.sales.models import Sale, SaleItem
from apps.purchases.models import Supplier, Purchase
from apps.prescriptions.models import Prescription

# ===============================
# 1. ACCOUNTS APP
# ===============================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )


# ===============================
# 2. INVENTORY APP
# ===============================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'medicine_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def medicine_count(self, obj):
        return obj.medicines.count()
    medicine_count.short_description = "Medicines"


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'brand', 'batch_number',
        'cost_price', 'selling_price', 'quantity',
        'expiry_date', 'is_low_stock', 'profit_margin_display'
    )
    list_filter = ('category', 'brand', 'expiry_date')
    search_fields = ('name', 'brand', 'batch_number')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'profit_margin_display')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'brand', 'batch_number')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price', 'profit_margin_display')
        }),
        ('Stock', {
            'fields': ('quantity', 'reorder_level')
        }),
        ('Dates', {
            'fields': ('expiry_date', 'created_at', 'updated_at')
        }),
    )
    
    def profit_margin_display(self, obj):
        if obj.cost_price and obj.cost_price > 0:
            margin = ((obj.selling_price - obj.cost_price) / obj.cost_price) * 100
            return f"{margin:.2f}%"
        return "N/A"
    profit_margin_display.short_description = "Profit Margin"
    
    def is_low_stock(self, obj):
        return obj.quantity <= obj.reorder_level
    is_low_stock.boolean = True
    is_low_stock.short_description = "Low Stock"
    
    actions = ['mark_as_restocked']
    
    def mark_as_restocked(self, request, queryset):
        updated = queryset.update(quantity=100)
        self.message_user(request, f'{updated} medicine(s) restocked to 100 units.')
    mark_as_restocked.short_description = "Restock selected (set qty to 100)"


# ===============================
# 3. SALES APP
# ===============================

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('medicine', 'quantity', 'price', 'subtotal')
    can_delete = False
    fields = ('medicine', 'quantity', 'price', 'subtotal')
    
    def subtotal(self, obj):
        return obj.quantity * obj.price
    subtotal.short_description = "Subtotal"
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_name', 'total', 'item_count', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('customer_name', 'user__username', 'items__medicine__name')
    ordering = ('-created_at',)
    readonly_fields = ('total', 'created_at')
    inlines = [SaleItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sale Information', {
            'fields': ('user', 'customer_name', 'total')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale_id', 'medicine', 'quantity', 'price', 'subtotal')
    list_filter = ('sale__created_at', 'medicine__category')
    search_fields = ('medicine__name', 'sale__customer_name', 'sale__id')
    
    def sale_id(self, obj):
        return f"Sale #{obj.sale.id}"
    sale_id.short_description = "Sale"
    
    def subtotal(self, obj):
        return obj.quantity * obj.price
    subtotal.short_description = "Subtotal"


# ===============================
# 4. PURCHASES APP
# ===============================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'purchase_count')
    search_fields = ('name', 'phone', 'email', 'contact_person')
    ordering = ('name',)
    
    fieldsets = (
        ('Supplier Information', {
            'fields': ('name', 'contact_person')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
    )
    
    def purchase_count(self, obj):
        return obj.purchases.count()
    purchase_count.short_description = "Purchases"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'supplier', 'quantity', 'cost_price', 'total_cost', 'date')
    list_filter = ('date', 'supplier', 'medicine__category')
    search_fields = ('medicine__name', 'supplier__name')
    ordering = ('-date',)
    readonly_fields = ('total_cost', 'date')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Purchase Details', {
            'fields': ('medicine', 'supplier', 'quantity', 'cost_price')
        }),
        ('Financial', {
            'fields': ('total_cost',)
        }),
        ('Date', {
            'fields': ('date',)
        }),
    )
    
    def total_cost(self, obj):
        return obj.quantity * obj.cost_price
    total_cost.short_description = "Total Cost"


# ===============================
# 5. PRESCRIPTIONS APP
# ===============================

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'doctor_name', 'image_preview', 'verified', 'created_at')
    list_filter = ('verified', 'created_at')
    search_fields = ('patient_name', 'doctor_name', 'notes')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'image_preview')
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_name', 'doctor_name')
        }),
        ('Prescription Details', {
            'fields': ('image', 'image_preview', 'notes')
        }),
        ('Status', {
            'fields': ('verified',)
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['verify_prescriptions', 'unverify_prescriptions']
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />'
        return "No image"
    image_preview.short_description = "Preview"
    image_preview.allow_tags = True
    
    def verify_prescriptions(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, f'{updated} prescription(s) verified successfully.')
    verify_prescriptions.short_description = "✅ Verify selected prescriptions"
    
    def unverify_prescriptions(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, f'{updated} prescription(s) marked as unverified.')
    unverify_prescriptions.short_description = "❌ Unverify selected prescriptions"


# ===============================
# CUSTOMIZE ADMIN SITE
# ===============================

admin.site.site_header = "Pharmacy Management System"
admin.site.site_title = "Shima PHAR Admin"
admin.site.index_title = "Welcome to Shima PHAR Administration"