import logging
from psycopg2 import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Produit, Categorie, ChampsPersonnalises, SousCategorie, Famille, SousFamille, Marque, Model
from .serializers import (
    ProduitSerializer, ProduitCreateUpdateSerializer, CategorieSerializer,
    ChampsPersonnalisesSerializer, SousCategorieSerializer,
    FamilleSerializer, SousFamilleSerializer, MarqueSerializer, ModelSerializer
)

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
    def _get_model_instance(self, model_class, name_field, name_value, parent=None, parent_field=None):
        if not name_value:
            return None

        filter_kwargs = {name_field: name_value}
        if parent and parent_field:
            filter_kwargs[parent_field] = parent

        try:
            instance = model_class.objects.get(**filter_kwargs)
            return instance
        except model_class.DoesNotExist:
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
                categorie = self._get_model_instance(Categorie, 'categorie', product.get('categorie', {}).get('categorie'))
                if not categorie:
                    raise ValueError(f"Categorie '{product.get('categorie', {}).get('categorie')}' not found in database")

                sous_categorie = self._get_model_instance(SousCategorie, 'sousCategorie', product.get('champsPersonnalises', {}).get('sousCategorie'), categorie, 'categorie')
                marque = self._get_model_instance(Marque, 'marque', product.get('champsPersonnalises', {}).get('marque'))
                model = self._get_model_instance(Model, 'model', product.get('champsPersonnalises', {}).get('model'), marque, 'marque') if marque else None
                famille = self._get_model_instance(Famille, 'famille', product.get('champsPersonnalises', {}).get('famille'))
                sous_famille = self._get_model_instance(SousFamille, 'sousFamille', product.get('champsPersonnalises', {}).get('sousFamille'), famille, 'famille') if famille else None

                champs_personnalises_data = {
                    'sousCategorie': getattr(sous_categorie, 'idSousCategorie', None),
                    'marque': getattr(marque, 'idMarque', None),
                    'model': getattr(model, 'idModel', None),
                    'famille': getattr(famille, 'idFamille', None),
                    'sousFamille': getattr(sous_famille, 'idSousFamille', None),
                    'taille': product.get('champsPersonnalises', {}).get('taille'),
                    'couleur': product.get('champsPersonnalises', {}).get('couleur'),
                    'poids': product.get('champsPersonnalises', {}).get('poids'),
                    'volume': product.get('champsPersonnalises', {}).get('volume'),
                    'dimensions': product.get('champsPersonnalises', {}).get('dimensions')
                }

                prix_vente = product.get("prixVenteTTC")
                if isinstance(prix_vente, str):
                    prix_vente = float(prix_vente.replace(',', '.'))

                product_data = {
                    "reference": product.get("reference"),
                    "type": product.get("type"),
                    "codeBarres": product.get("codeBarres"),
                    "uniteType": product.get("uniteType"),
                    "prixVenteTTC": prix_vente if prix_vente else 0,
                    "description": product.get("description") or "",
                    "categorie": categorie.idCategorie if categorie else None,
                    "champsPersonnalises": champs_personnalises_data
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