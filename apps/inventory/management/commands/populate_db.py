from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from apps.accounts.models import User
from apps.inventory.models import Category, Medicine
from apps.purchases.models import Supplier, Purchase
from apps.sales.models import Sale, SaleItem
from apps.prescriptions.models import Prescription

class Command(BaseCommand):
    help = 'Populate database with default sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating default data...')

        # Users
        if not User.objects.filter(email='admin@pharmacy.com').exists():
            admin = User.objects.create_superuser(
                username='admin', email='admin@pharmacy.com',
                password='admin123', role='admin',
                first_name='System', last_name='Admin'
            )
            self.stdout.write(f'Created admin: {admin.username}')
        else:
            admin = User.objects.get(email='admin@pharmacy.com')

        if not User.objects.filter(email='pharmacist@pharmacy.com').exists():
            pharmacist = User.objects.create_user(
                username='pharmacist', email='pharmacist@pharmacy.com',
                password='pharma123', role='pharmacist',
                first_name='John', last_name='Doe'
            )
            self.stdout.write(f'Created pharmacist: {pharmacist.username}')
        else:
            pharmacist = User.objects.get(email='pharmacist@pharmacy.com')

        # Categories
        categories = {}
        for name in ['Tablets', 'Capsules', 'Syrups', 'Injectables', 'Ointments', 'Drops', 'Inhalers']:
            obj, created = Category.objects.get_or_create(name=name)
            categories[name] = obj
            if created:
                self.stdout.write(f'Created category: {name}')

        # Suppliers
        suppliers = {}
        supplier_data = [
            {'name': 'MediCorp Ltd', 'contact_person': 'Robert Brown', 'phone': '1234567890', 'email': 'robert@medicorp.com', 'address': '123 Pharma St'},
            {'name': 'HealthPlus Distributors', 'contact_person': 'Sarah Wilson', 'phone': '0987654321', 'email': 'sarah@healthplus.com', 'address': '456 Care Ave'},
            {'name': 'GlobalMeds Inc', 'contact_person': 'Mike Johnson', 'phone': '1122334455', 'email': 'mike@globalmeds.com', 'address': '789 Wellness Rd'},
        ]
        for s in supplier_data:
            obj, created = Supplier.objects.get_or_create(name=s['name'], defaults=s)
            suppliers[s['name']] = obj
            if created:
                self.stdout.write(f'Created supplier: {obj.name}')

        # Medicines with cost_price and selling_price
        medicine_list = [
            {'name': 'Paracetamol 500mg', 'category': 'Tablets', 'brand': 'PharmaCo', 'batch': 'P500-2024', 'expiry': date.today() + timedelta(days=365), 'cost': Decimal('0.35'), 'selling': Decimal('0.50'), 'qty': 200, 'reorder': 50},
            {'name': 'Amoxicillin 250mg', 'category': 'Capsules', 'brand': 'BioCure', 'batch': 'AMX-101', 'expiry': date.today() + timedelta(days=180), 'cost': Decimal('0.90'), 'selling': Decimal('1.20'), 'qty': 45, 'reorder': 40},
            {'name': 'Ibuprofen 400mg', 'category': 'Tablets', 'brand': 'PainRelief', 'batch': 'IBU-2025', 'expiry': date.today() + timedelta(days=700), 'cost': Decimal('0.55'), 'selling': Decimal('0.80'), 'qty': 15, 'reorder': 30},
            {'name': 'Cough Syrup', 'category': 'Syrups', 'brand': 'SoothRx', 'batch': 'CS-99', 'expiry': date.today() + timedelta(days=90), 'cost': Decimal('2.50'), 'selling': Decimal('3.50'), 'qty': 30, 'reorder': 20},
            {'name': 'Insulin Glargine', 'category': 'Injectables', 'brand': 'DiaCare', 'batch': 'INS-881', 'expiry': date.today() + timedelta(days=365), 'cost': Decimal('18.00'), 'selling': Decimal('25.00'), 'qty': 12, 'reorder': 10},
            {'name': 'Omeprazole 20mg', 'category': 'Capsules', 'brand': 'GastroHeal', 'batch': 'OME-234', 'expiry': date.today() + timedelta(days=400), 'cost': Decimal('0.65'), 'selling': Decimal('0.90'), 'qty': 80, 'reorder': 40},
            {'name': 'Cetirizine 10mg', 'category': 'Tablets', 'brand': 'AllerGo', 'batch': 'CET-567', 'expiry': date.today() + timedelta(days=250), 'cost': Decimal('0.40'), 'selling': Decimal('0.60'), 'qty': 55, 'reorder': 30},
            {'name': 'Azithromycin 500mg', 'category': 'Tablets', 'brand': 'ZithroMax', 'batch': 'AZI-123', 'expiry': date.today() + timedelta(days=60), 'cost': Decimal('1.80'), 'selling': Decimal('2.50'), 'qty': 25, 'reorder': 30},
            {'name': 'Salbutamol Inhaler', 'category': 'Inhalers', 'brand': 'BreatheEasy', 'batch': 'SAL-998', 'expiry': date.today() + timedelta(days=540), 'cost': Decimal('6.00'), 'selling': Decimal('8.00'), 'qty': 40, 'reorder': 15},
            {'name': 'Hydrocortisone Cream', 'category': 'Ointments', 'brand': 'DermaRelief', 'batch': 'HYD-442', 'expiry': date.today() + timedelta(days=365), 'cost': Decimal('3.00'), 'selling': Decimal('4.50'), 'qty': 18, 'reorder': 20},
            {'name': 'Vitamin C 500mg', 'category': 'Tablets', 'brand': 'VitaMax', 'batch': 'VIT-112', 'expiry': date.today() + timedelta(days=800), 'cost': Decimal('0.20'), 'selling': Decimal('0.30'), 'qty': 350, 'reorder': 100},
            {'name': 'Metformin 500mg', 'category': 'Tablets', 'brand': 'GlucoGuard', 'batch': 'MET-776', 'expiry': date.today() + timedelta(days=600), 'cost': Decimal('0.50'), 'selling': Decimal('0.70'), 'qty': 90, 'reorder': 50},
            {'name': 'Eye Drops', 'category': 'Drops', 'brand': 'ClearSight', 'batch': 'EYE-333', 'expiry': date.today() + timedelta(days=180), 'cost': Decimal('3.50'), 'selling': Decimal('5.00'), 'qty': 22, 'reorder': 15},
            {'name': 'Multivitamin Syrup', 'category': 'Syrups', 'brand': 'NutriBoost', 'batch': 'MVS-765', 'expiry': date.today() + timedelta(days=400), 'cost': Decimal('2.80'), 'selling': Decimal('4.00'), 'qty': 35, 'reorder': 25},
        ]

        medicines = {}
        for med in medicine_list:
            cat = categories[med['category']]
            obj, created = Medicine.objects.get_or_create(
                name=med['name'], brand=med['brand'],
                defaults={
                    'category': cat,
                    'batch_number': med['batch'],
                    'expiry_date': med['expiry'],
                    'cost_price': med['cost'],
                    'selling_price': med['selling'],
                    'quantity': med['qty'],
                    'reorder_level': med['reorder']
                }
            )
            medicines[obj.name] = obj
            if created:
                self.stdout.write(f'Created medicine: {obj.name}')

        # Purchases
        if Purchase.objects.count() == 0:
            purchase_data = [
                {'supplier': 'MediCorp Ltd', 'medicine': 'Paracetamol 500mg', 'quantity': 100, 'cost': Decimal('0.35')},
                {'supplier': 'HealthPlus Distributors', 'medicine': 'Amoxicillin 250mg', 'quantity': 50, 'cost': Decimal('0.90')},
                {'supplier': 'MediCorp Ltd', 'medicine': 'Ibuprofen 400mg', 'quantity': 30, 'cost': Decimal('0.55')},
                {'supplier': 'GlobalMeds Inc', 'medicine': 'Insulin Glargine', 'quantity': 20, 'cost': Decimal('18.00')},
            ]
            for p in purchase_data:
                Purchase.objects.create(
                    supplier=suppliers[p['supplier']],
                    medicine=medicines[p['medicine']],
                    quantity=p['quantity'],
                    cost_price=p['cost']
                )
            self.stdout.write('Created purchase records')

        # Sales
        if Sale.objects.count() == 0:
            sale1 = Sale.objects.create(user=pharmacist, customer_name='Alice Smith', total=0)
            items1 = [
                {'medicine': medicines['Paracetamol 500mg'], 'quantity': 2, 'price': Decimal('0.50')},
                {'medicine': medicines['Ibuprofen 400mg'], 'quantity': 1, 'price': Decimal('0.80')},
            ]
            total1 = Decimal('0')
            for item in items1:
                med = item['medicine']
                if med.quantity >= item['quantity']:
                    med.quantity -= item['quantity']
                    med.save()
                    SaleItem.objects.create(sale=sale1, medicine=med, quantity=item['quantity'], price=item['price'])
                    total1 += item['price'] * item['quantity']
            sale1.total = total1
            sale1.save()
            sale1.created_at = timezone.now() - timedelta(days=1)
            sale1.save()

            sale2 = Sale.objects.create(user=pharmacist, customer_name='Bob Jones', total=0)
            items2 = [
                {'medicine': medicines['Cough Syrup'], 'quantity': 2, 'price': Decimal('3.50')},
                {'medicine': medicines['Amoxicillin 250mg'], 'quantity': 3, 'price': Decimal('1.20')},
            ]
            total2 = Decimal('0')
            for item in items2:
                med = item['medicine']
                if med.quantity >= item['quantity']:
                    med.quantity -= item['quantity']
                    med.save()
                    SaleItem.objects.create(sale=sale2, medicine=med, quantity=item['quantity'], price=item['price'])
                    total2 += item['price'] * item['quantity']
            sale2.total = total2
            sale2.save()
            self.stdout.write('Created sales records')

        # Prescription
        if not Prescription.objects.exists():
            Prescription.objects.create(
                patient_name='Emma Watson',
                doctor_name='Dr. Gregory House',
                notes='Take two tablets daily after meals.',
                verified=False
            )
            self.stdout.write('Created sample prescription')

        self.stdout.write(self.style.SUCCESS('Default data populated successfully!'))