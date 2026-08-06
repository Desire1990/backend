from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from apps.inventory.views import MedicineViewSet, CategoryViewSet
from apps.sales.views import SaleViewSet
from apps.purchases.views import SupplierViewSet, PurchaseViewSet
from apps.prescriptions.views import PrescriptionViewSet
from apps.dashboard.views import DashboardView
from . import views

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'prescriptions', PrescriptionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/', include(router.urls)),
    re_path("^.*$", views.index),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
