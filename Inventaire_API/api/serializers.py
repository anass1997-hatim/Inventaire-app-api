from rest_framework import serializers
from .models import (
    Produit, Categorie, ChampsPersonnalises,
    SousCategorie, Famille, SousFamille, Marque, Model, TypeProduit, UniteType, TagTid
)

class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie
        fields = ['idSousCategorie', 'sousCategorie', 'categorie']

class FamilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famille
        fields = ['idFamille', 'famille']

class SousFamilleSerializer(serializers.ModelSerializer):
    famille = FamilleSerializer()
    class Meta:
        model = SousFamille
        fields = ['idSousFamille', 'sousFamille', 'famille']

class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = ['idMarque', 'marque']

class ModelSerializer(serializers.ModelSerializer):
    marque = MarqueSerializer()
    class Meta:
        model = Model
        fields = ['idModel', 'model', 'marque']

class TypeProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduit
        fields = ['id', 'nom']

class UniteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniteType
        fields = ['id', 'nom']

class ChampsPersonnalisesSerializer(serializers.ModelSerializer):
    sousCategorie = SousCategorieSerializer(read_only=True)
    marque = MarqueSerializer(read_only=True)
    model = ModelSerializer(read_only=True)
    famille = FamilleSerializer(read_only=True)
    sousFamille = SousFamilleSerializer(read_only=True)
    class Meta:
        model = ChampsPersonnalises
        fields = [
            'idChampsPersonnalises', 'sousCategorie', 'marque', 'model',
            'famille', 'sousFamille', 'taille', 'couleur', 'poids', 'volume', 'dimensions'
        ]

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['idCategorie', 'categorie']

class ProduitSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    champsPersonnalises = ChampsPersonnalisesSerializer(read_only=True)
    type = TypeProduitSerializer(read_only=True)
    uniteType = UniteTypeSerializer(read_only=True)
    class Meta:
        model = Produit
        fields = [
            'reference', 'type', 'codeBarres', 'uniteType', 'prixVenteTTC', 'description',
            'categorie', 'champsPersonnalises', 'dateCreation'
        ]

class ChampsPersonnalisesCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampsPersonnalises
        fields = [
            'sousCategorie', 'marque', 'model',
            'famille', 'sousFamille', 'taille',
            'couleur', 'poids', 'volume', 'dimensions'
        ]

    def validate(self, attrs):
        pk_mapping = {
            'sousCategorie': ('idSousCategorie', SousCategorie),
            'marque': ('idMarque', Marque),
            'model': ('idModel', Model),
            'famille': ('idFamille', Famille),
            'sousFamille': ('idSousFamille', SousFamille)
        }

        for field in pk_mapping:
            if field in attrs and attrs[field]:
                pk_name, model_class = pk_mapping[field]
                pk_value = getattr(attrs[field], pk_name)
                if not model_class.objects.filter(**{pk_name: pk_value}).exists():
                    raise serializers.ValidationError({
                        field: f"{field} with {pk_name}={pk_value} does not exist."
                    })
        return attrs

class ProduitCreateUpdateSerializer(serializers.ModelSerializer):
    champsPersonnalises = ChampsPersonnalisesCreateUpdateSerializer(required=False)
    type = serializers.PrimaryKeyRelatedField(queryset=TypeProduit.objects.all())
    uniteType = serializers.PrimaryKeyRelatedField(queryset=UniteType.objects.all())
    class Meta:
        model = Produit
        fields = [
            'reference', 'type', 'codeBarres', 'uniteType',
            'prixVenteTTC', 'description', 'categorie',
            'champsPersonnalises'
        ]

    def create(self, validated_data):
        champs_personnalises_data = validated_data.pop('champsPersonnalises', None)
        produit = Produit.objects.create(**validated_data)

        if champs_personnalises_data:
            cleaned_data = {}
            for key, value in champs_personnalises_data.items():
                if value == "":
                    cleaned_data[key] = None
                else:
                    if key in ['sousCategorie', 'marque', 'model', 'famille', 'sousFamille']:
                        cleaned_data[key] = value
                    else:
                        cleaned_data[key] = value

            champs_personnalises = ChampsPersonnalises.objects.create(**cleaned_data)
            produit.champsPersonnalises = champs_personnalises
            produit.save()

        return produit

    def update(self, instance, validated_data):
        champs_personnalises_data = validated_data.pop('champsPersonnalises', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if champs_personnalises_data:
            cleaned_data = {}
            for key, value in champs_personnalises_data.items():
                if value == "":
                    cleaned_data[key] = None
                else:
                    if key in ['sousCategorie', 'marque', 'model', 'famille', 'sousFamille']:
                        cleaned_data[key] = value
                    else:
                        cleaned_data[key] = value

            if instance.champsPersonnalises:
                for attr, val in cleaned_data.items():
                    setattr(instance.champsPersonnalises, attr, val)
                instance.champsPersonnalises.save()
            else:
                champs_personnalises = ChampsPersonnalises.objects.create(**cleaned_data)
                instance.champsPersonnalises = champs_personnalises

        instance.save()
        return instance




class TagTidSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagTid
        fields = ['tid', 'epc', 'user']



class ProductSuggestionSerializer(serializers.Serializer):
    reference = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField(allow_null=True)
    brand = serializers.CharField(allow_null=True)
    model = serializers.CharField(allow_null=True)
    type = serializers.CharField(allow_null=True)
    unit_type = serializers.CharField(allow_null=True)