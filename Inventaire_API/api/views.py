from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Produit, Categorie, Depot, ChampsPersonnalises
from .serializers import ProduitSerializer, CategorieSerializer, DepotSerializer

class ProduitViewSet(ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    lookup_field = 'reference'
    lookup_url_kwarg = 'reference'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers={"Location": f"/produits/{serializer.instance.pk}"}
        )

    def update(self, request, reference=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class CategorieViewSet(ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class DepotViewSet(ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer


EXCEL_TO_JSON_MAPPING = {
    "Référence": "reference",
    "Type": "type",
    "Code Barres": "codeBarres",
    "Unité Type": "uniteType",
    "Prix Vente TTC": "prixVenteTTC",
    "Description": "description",
    "Catégorie": "categorie",
    "Dépôt": "depot",
    "Quantité": "quantite",
    "Code RFID": "codeRFID",
    "Date Affectation": "dateAffectation",
    "Date Péremption": "datePeremption"
}


def preprocess_excel_data(data):
    processed_data = []
    for row in data:
        processed_row = {EXCEL_TO_JSON_MAPPING.get(key, key): value for key, value in row.items()}
        processed_data.append(processed_row)
    return processed_data


import logging

logger = logging.getLogger(__name__)


class BulkUploadView(APIView):
    def post(self, request):
        raw_products = request.data.get('products', [])
        if not isinstance(raw_products, list):
            return Response(
                {'error': 'Invalid data format. Expected a list of products.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = preprocess_excel_data(raw_products)
        validation_results = []
        created_products = []

        for product in products:
            try:
                # Debug incoming data
                logger.debug(f"Processing product: {product}")

                # Process "categorie"
                categorie_data = product.get('categorie', {})
                if isinstance(categorie_data, dict):
                    categorie, created = Categorie.objects.get_or_create(
                        categorie=categorie_data.get('categorie')
                    )
                elif isinstance(categorie_data, str):
                    categorie, created = Categorie.objects.get_or_create(
                        categorie=categorie_data
                    )
                else:
                    raise ValueError("Invalid categorie format.")

                categorie_dict = {
                    'idCategorie': categorie.idCategorie,
                    'categorie': categorie.categorie
                }

                # Process "depot"
                depot_data = product.get('depot', {})
                if isinstance(depot_data, dict):
                    depot, created = Depot.objects.get_or_create(
                        depot=depot_data.get('depot')
                    )
                elif isinstance(depot_data, str):
                    depot, created = Depot.objects.get_or_create(
                        depot=depot_data
                    )
                else:
                    raise ValueError("Invalid depot format.")

                depot_dict = {
                    'idDepot': depot.idDepot,
                    'depot': depot.depot
                }

                # Process "champsPersonnalises"
                champs_personnalises_data = product.get('champsPersonnalises')
                champs_personnalises_dict = None

                logger.debug(f"champs_personnalises_data: {champs_personnalises_data}")

                if champs_personnalises_data:
                    champs_personnalises = ChampsPersonnalises.objects.create(
                        sousCategorie=champs_personnalises_data.get('sousCategorie'),
                        marque=champs_personnalises_data.get('marque'),
                        model=champs_personnalises_data.get('model'),
                        famille=champs_personnalises_data.get('famille'),
                        sousFamille=champs_personnalises_data.get('sousFamille'),
                        taille=champs_personnalises_data.get('taille'),
                        couleur=champs_personnalises_data.get('couleur'),
                        poids=champs_personnalises_data.get('poids'),
                        volume=champs_personnalises_data.get('volume'),
                        dimensions=champs_personnalises_data.get('dimensions')
                    )

                    champs_personnalises_dict = {
                        'idChampsPersonnales': champs_personnalises.idChampsPersonnales,
                        'sousCategorie': champs_personnalises.sousCategorie,
                        'marque': champs_personnalises.marque,
                        'model': champs_personnalises.model,
                        'famille': champs_personnalises.famille,
                        'sousFamille': champs_personnalises.sousFamille,
                        'taille': champs_personnalises.taille,
                        'couleur': champs_personnalises.couleur,
                        'poids': champs_personnalises.poids,
                        'volume': champs_personnalises.volume,
                        'dimensions': champs_personnalises.dimensions
                    }

                logger.debug(f"champs_personnalises_dict: {champs_personnalises_dict}")

                # Prepare product data
                product_data = {
                    'reference': product.get('reference'),
                    'type': product.get('type'),
                    'codeBarres': product.get('codeBarres'),
                    'description': product.get('description'),
                    'uniteType': product.get('uniteType'),
                    'prixVenteTTC': product.get('prixVenteTTC'),
                    'quantite': int(product.get('quantite', 0)),
                    'codeRFID': product.get('codeRFID', ''),
                    'dateAffectation': product.get('dateAffectation'),
                    'datePeremption': product.get('datePeremption'),
                    'categorie': categorie_dict,
                    'depot': depot_dict,
                }

                # Add "champsPersonnalises" if present
                if champs_personnalises_dict:
                    product_data['champsPersonnalises'] = champs_personnalises_dict

                # Debug final product data
                logger.debug(f"Final product_data: {product_data}")

                # Validate and save the product
                serializer = ProduitSerializer(data=product_data)
                if serializer.is_valid():
                    serializer.save()
                    created_products.append(serializer.data)
                else:
                    validation_results.append({
                        'data': product,
                        'errors': serializer.errors
                    })
                    logger.error(f"Validation errors: {serializer.errors}")

            except Exception as e:
                logger.error(f"Error processing product: {str(e)}")
                validation_results.append({
                    'data': product,
                    'error': str(e)
                })

        # Return response
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
