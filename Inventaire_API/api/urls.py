from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from django.urls import path, include
from .views import (
    ProduitViewSet, CategorieViewSet, ChampsPersonnalisesViewSet,
    SousCategorieViewSet, FamilleViewSet, SousFamilleViewSet,
    MarqueViewSet, ModelViewSet, BulkUploadView, TypeProduitViewSet, UniteTypeViewSet, TagTidViewSet, ProductSearchView
)

# Main router
router = DefaultRouter()
router.register(r'produits', ProduitViewSet, basename='produits')
router.register(r'categories', CategorieViewSet, basename='categories')
router.register(r'champs-personnalises', ChampsPersonnalisesViewSet, basename='champs-personnalises')
router.register(r'familles', FamilleViewSet, basename='familles')
router.register(r'sous-familles', SousFamilleViewSet, basename='sous-familles')
router.register(r'marques', MarqueViewSet, basename='marques')
router.register(r'modeles', ModelViewSet, basename='modeles')
router.register(r'sous-categories', SousCategorieViewSet, basename='sous-categories')
router.register(r'types-produit', TypeProduitViewSet, basename='types-produit')
router.register(r'unites-type', UniteTypeViewSet, basename='unites-type')

categories_router = NestedSimpleRouter(router, r'categories', lookup='categorie')
categories_router.register(r'sous-categories', SousCategorieViewSet, basename='categorie-sous-categories')

familles_router = NestedSimpleRouter(router, r'familles', lookup='famille')
familles_router.register(r'sous-familles', SousFamilleViewSet, basename='famille-sous-familles')

marques_router = NestedSimpleRouter(router, r'marques', lookup='marque')
marques_router.register(r'modeles', ModelViewSet, basename='marque-modeles')


router.register(r'tagtid', TagTidViewSet, basename='tagtid')


urlpatterns = [
    path('produits/bulk-upload/', BulkUploadView.as_view(), name='bulk-upload'),
    path('rechercher/', ProductSearchView.as_view(), name='product_search'),
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
    path('', include(familles_router.urls)),
    path('', include(marques_router.urls)),
]