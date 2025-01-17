from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduitViewSet, CategorieViewSet, DepotViewSet, BulkUploadView

router = DefaultRouter()
router.register('produits', ProduitViewSet)
router.register('categories', CategorieViewSet)
router.register('depots', DepotViewSet)

urlpatterns = [
    path('produits/upload/', BulkUploadView.as_view(), name='bulk_upload'),
    path('', include(router.urls)),
]