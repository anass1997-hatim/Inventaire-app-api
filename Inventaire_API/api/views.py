import logging

from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Produit, Categorie, ChampsPersonnalises, SousCategorie, Famille, SousFamille, Marque, Model, \
    TypeProduit, UniteType, TagTid
from .serializers import (
    ProduitSerializer, ProduitCreateUpdateSerializer, CategorieSerializer,
    ChampsPersonnalisesSerializer, SousCategorieSerializer,
    FamilleSerializer, SousFamilleSerializer, MarqueSerializer, ModelSerializer, TypeProduitSerializer,
    UniteTypeSerializer, TagTidSerializer, ProductSuggestionSerializer
)
from .services.services import search_product_suggestions


class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    lookup_field = 'reference'
    serializer_class = ProduitSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProduitCreateUpdateSerializer
        return ProduitSerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    lookup_field = 'idCategorie'

class ChampsPersonnalisesViewSet(viewsets.ModelViewSet):
    queryset = ChampsPersonnalises.objects.all()
    serializer_class = ChampsPersonnalisesSerializer
    lookup_field = 'idChampsPersonnalises'

class SousCategorieViewSet(ModelViewSet):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer

    def get_queryset(self):
        categorie_id = self.kwargs.get('categorie_idCategorie')
        if categorie_id:
            return self.queryset.filter(categorie_id=categorie_id)
        return self.queryset

class FamilleViewSet(viewsets.ModelViewSet):
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer
    lookup_field = 'idFamille'

class SousFamilleViewSet(viewsets.ModelViewSet):
    queryset = SousFamille.objects.all()
    serializer_class = SousFamilleSerializer
    lookup_field = 'idSousFamille'

    def get_queryset(self):
        famille_id = self.kwargs.get('famille_idFamille')
        if famille_id:
            return self.queryset.filter(famille_id=famille_id)
        return self.queryset

class MarqueViewSet(viewsets.ModelViewSet):
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer
    lookup_field = 'idMarque'

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    lookup_field = 'idModel'

    def get_queryset(self):
        marque_id = self.kwargs.get('marque_idMarque')
        if marque_id:
            return self.queryset.filter(marque_id=marque_id)
        return self.queryset

class TypeProduitViewSet(viewsets.ModelViewSet):
    queryset = TypeProduit.objects.all()
    serializer_class = TypeProduitSerializer
    lookup_field = 'id'

class UniteTypeViewSet(viewsets.ModelViewSet):
    queryset = UniteType.objects.all()
    serializer_class = UniteTypeSerializer
    lookup_field = 'id'

def preprocess_excel_data(data):
    EXCEL_TO_JSON_MAPPING = {
        "Référence": "reference",
        "Type": "type",
        "Code Barres": "codeBarres",
        "Unité Type": "uniteType",
        "Prix Vente TTC": "prixVenteTTC",
        "Description": "description",
        "Catégorie": "categorie",
        "Sous Catégorie": "sousCategorie",
        "Marque": "marque",
        "Model": "model",
        "Famille": "famille",
        "Sous Famille": "sousFamille",
        "Taille": "taille",
        "Couleur": "couleur",
        "Poids": "poids",
        "Volume": "volume",
        "Dimensions": "dimensions"
    }

    processed_data = []
    for row in data:
        processed_row = {
            EXCEL_TO_JSON_MAPPING.get(key, key): value for key, value in row.items()
        }
        processed_data.append(processed_row)
    return processed_data


class BulkUploadView(APIView):
    def _get_or_create_instance(self, model_class, lookup_field, lookup_value,
                                parent=None, parent_field=None,
                                create_if_not_exists=True):
        if not lookup_value:
            return None

        filter_kwargs = {lookup_field: lookup_value}
        if parent and parent_field:
            filter_kwargs[parent_field] = parent

        try:
            return model_class.objects.get(**filter_kwargs)
        except model_class.DoesNotExist:
            if create_if_not_exists:
                return model_class.objects.create(**filter_kwargs)
            else:
                return None

    def post(self, request):
        raw_products = request.data.get('products', [])
        if not isinstance(raw_products, list):
            return Response(
                {'error': 'Invalid data format. Expected a list of products.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = preprocess_excel_data(raw_products)

        created_products = []
        validation_results = []

        for product in products:
            try:
                type_str = product.get('type', None)
                type_obj = self._get_or_create_instance(
                    TypeProduit, 'nom', type_str, create_if_not_exists=True
                )

                unite_str = product.get('uniteType', None)
                unite_obj = self._get_or_create_instance(
                    UniteType, 'nom', unite_str, create_if_not_exists=True
                )

                cat_data = product.get('categorie', {})
                cat_name = cat_data.get('categorie')
                categorie = self._get_or_create_instance(
                    Categorie, 'categorie', cat_name, create_if_not_exists=True
                )

                champs_data = product.get('champsPersonnalises', {})

                sous_cat_name = champs_data.get('sousCategorie')
                sous_categorie = self._get_or_create_instance(
                    SousCategorie,
                    'sousCategorie',
                    sous_cat_name,
                    parent=categorie,
                    parent_field='categorie',
                    create_if_not_exists=True
                )

                marque_name = champs_data.get('marque')
                marque_obj = self._get_or_create_instance(
                    Marque, 'marque', marque_name, create_if_not_exists=True
                )

                model_name = champs_data.get('model')
                model_obj = None
                if model_name:
                    model_obj = self._get_or_create_instance(
                        Model,
                        'model',
                        model_name,
                        parent=marque_obj,
                        parent_field='marque',
                        create_if_not_exists=True
                    )

                famille_name = champs_data.get('famille')
                famille_obj = self._get_or_create_instance(
                    Famille, 'famille', famille_name, create_if_not_exists=True
                )

                sous_famille_name = champs_data.get('sousFamille')
                sous_famille_obj = None
                if sous_famille_name:
                    sous_famille_obj = self._get_or_create_instance(
                        SousFamille,
                        'sousFamille',
                        sous_famille_name,
                        parent=famille_obj,
                        parent_field='famille',
                        create_if_not_exists=True
                    )

                prix_vente = product.get("prixVenteTTC", 0)
                if isinstance(prix_vente, str):
                    prix_vente = float(prix_vente.replace(',', '.'))

                product_data = {
                    "reference": product.get("reference"),
                    "type": type_obj.id if type_obj else None,
                    "codeBarres": product.get("codeBarres") or "",
                    "uniteType": unite_obj.id if unite_obj else None,
                    "prixVenteTTC": prix_vente,
                    "description": product.get("description") or "",
                    "categorie": categorie.idCategorie if categorie else None,
                    "champsPersonnalises": {
                        "sousCategorie": sous_categorie.idSousCategorie if sous_categorie else None,
                        "marque": marque_obj.idMarque if marque_obj else None,
                        "model": model_obj.idModel if model_obj else None,
                        "famille": famille_obj.idFamille if famille_obj else None,
                        "sousFamille": sous_famille_obj.idSousFamille if sous_famille_obj else None,
                        "taille": champs_data.get('taille') or None,
                        "couleur": champs_data.get('couleur') or None,
                        "poids": champs_data.get('poids') or None,
                        "volume": champs_data.get('volume') or None,
                        "dimensions": champs_data.get('dimensions') or None
                    }
                }

                serializer = ProduitCreateUpdateSerializer(data=product_data)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = ProduitSerializer(serializer.instance)
                    created_products.append(response_serializer.data)
                else:
                    validation_results.append({
                        'data': product,
                        'errors': serializer.errors
                    })

            except Exception as e:
                validation_results.append({
                    'data': product,
                    'errors': str(e)
                })

        if not created_products:
            return Response(
                {
                    'status': 'error',
                    'message': 'No valid products found.',
                    'validation_errors': validation_results
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'status': 'success',
                'message': f'{len(created_products)} products created successfully.',
                'created_products': created_products,
                'failed_validations': validation_results
            },
            status=status.HTTP_201_CREATED
        )



class TagTidViewSet(ModelViewSet):
    serializer_class = TagTidSerializer
    def get_queryset(self):
        return TagTid.objects.all().order_by('tid')



class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        suggestions = search_product_suggestions(query)
        serializer = ProductSuggestionSerializer(suggestions, many=True)
        return JsonResponse(serializer.data, safe=False)