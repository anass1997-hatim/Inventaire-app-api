from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .models import Produit, Categorie, Depot, ChampsPersonnalises

class ChampsPersonnalisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampsPersonnalises
        fields = [
            'idChampsPersonnales', 'sousCategorie', 'marque', 'model', 'famille', 'sousFamille',
            'taille', 'couleur', 'poids', 'volume', 'dimensions'
        ]
        read_only_fields = ['idChampsPersonnales']

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['idCategorie', 'categorie']

class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = ['idDepot', 'depot']

class ProduitSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer()
    depot = DepotSerializer()
    champsPersonnalises = ChampsPersonnalisesSerializer(required=False, allow_null=True)

    class Meta:
        model = Produit
        fields = [
            'reference', 'type', 'codeBarres', 'description', 'uniteType',
            'prixVenteTTC', 'categorie', 'depot', 'quantite', 'codeRFID',
            'dateAffectation', 'datePeremption', 'champsPersonnalises'
        ]

    def create(self, validated_data):
        categorie_data = validated_data.pop('categorie')
        depot_data = validated_data.pop('depot')
        champs_personnalises_data = validated_data.pop('champsPersonnalises', None)
        categorie, _ = Categorie.objects.get_or_create(**categorie_data)
        depot, _ = Depot.objects.get_or_create(**depot_data)
        champs_personnalises = None
        if champs_personnalises_data:
            champs_personnalises, _ = ChampsPersonnalises.objects.get_or_create(**champs_personnalises_data)
        produit = Produit.objects.create(
            categorie=categorie,
            depot=depot,
            champsPersonnalises=champs_personnalises,
            **validated_data
        )
        return produit

    def update(self, instance, validated_data):
        categorie_data = validated_data.pop('categorie', None)
        depot_data = validated_data.pop('depot', None)
        champs_personnalises_data = validated_data.pop('champsPersonnalises', None)
        if categorie_data:
            categorie, _ = Categorie.objects.get_or_create(
                categorie=categorie_data.get('categorie'),
                defaults={'idCategorie': categorie_data.get('idCategorie')}
            )
            instance.categorie = categorie
        if depot_data:
            depot, _ = Depot.objects.get_or_create(
                depot=depot_data.get('depot'),
                defaults={'idDepot': depot_data.get('idDepot')}
            )
            instance.depot = depot
        if champs_personnalises_data is not None:
            if instance.champsPersonnalises:
                for key, value in champs_personnalises_data.items():
                    setattr(instance.champsPersonnalises, key, value)
                instance.champsPersonnalises.save()
            else:
                champs_personnalises = ChampsPersonnalises.objects.create(**champs_personnalises_data)
                instance.champsPersonnalises = champs_personnalises
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    lookup_field = 'reference'
    lookup_url_kwarg = 'reference'

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


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    lookup_field = 'idCategorie'

class DepotViewSet(viewsets.ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer
    lookup_field = 'idDepot'

