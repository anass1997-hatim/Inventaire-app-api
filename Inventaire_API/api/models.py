from django.db import models
class TypeProduit(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = "type_produit"


class UniteType(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = "unite_type"


class Produit(models.Model):
    reference = models.CharField(max_length=100, primary_key=True)
    type = models.ForeignKey(
        'TypeProduit', on_delete=models.SET_NULL, null=True, related_name='produits'
    )
    codeBarres = models.CharField(max_length=100)
    uniteType = models.ForeignKey(
        'UniteType', on_delete=models.SET_NULL, null=True, related_name='produits'
    )
    prixVenteTTC = models.FloatField()
    description = models.TextField()
    categorie = models.ForeignKey(
        'Categorie', on_delete=models.CASCADE,
        related_name='produits', null=True
    )
    champsPersonnalises = models.ForeignKey(
        'ChampsPersonnalises', on_delete=models.CASCADE,
        related_name='produits', null=True
    )
    dateCreation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "produit"


class Categorie(models.Model):
    idCategorie = models.BigAutoField(primary_key=True)
    categorie = models.CharField(max_length=100)

    def __str__(self):
        return self.categorie

    class Meta:
        db_table = "categorie"


class Depot(models.Model):
    idDepot = models.BigAutoField(primary_key=True)
    depot = models.CharField(max_length=100)

    def __str__(self):
        return self.depot

    class Meta:
        db_table = "depot"


class ChampsPersonnalises(models.Model):
    idChampsPersonnalises = models.BigAutoField(primary_key=True)
    sousCategorie = models.ForeignKey(
        'SousCategorie', on_delete=models.SET_NULL, null=True, related_name="champs"
    )
    marque = models.ForeignKey(
        'Marque', on_delete=models.SET_NULL, null=True, related_name="champs"
    )
    model = models.ForeignKey(
        'Model', on_delete=models.SET_NULL, null=True, related_name="champs"
    )
    famille = models.ForeignKey(
        'Famille', on_delete=models.SET_NULL, null=True, related_name="champs"
    )
    sousFamille = models.ForeignKey(
        'SousFamille', on_delete=models.SET_NULL, null=True, related_name="champs"
    )
    taille = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    poids = models.CharField(max_length=100, null=True)
    volume = models.CharField(max_length=100, null=True)
    dimensions = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "champs_personnalises"


class SousCategorie(models.Model):
    idSousCategorie = models.BigAutoField(primary_key=True)
    sousCategorie = models.CharField(max_length=100)
    categorie = models.ForeignKey(
        'Categorie', on_delete=models.CASCADE, related_name="sousCategories"
    )

    def __str__(self):
        return self.sousCategorie

    class Meta:
        db_table = "sous_categorie"


class Famille(models.Model):
    idFamille = models.BigAutoField(primary_key=True)
    famille = models.CharField(max_length=100)

    def __str__(self):
        return self.famille

    class Meta:
        db_table = "famille"


class SousFamille(models.Model):
    idSousFamille = models.BigAutoField(primary_key=True)
    sousFamille = models.CharField(max_length=100)
    famille = models.ForeignKey(
        'Famille', on_delete=models.CASCADE, related_name="sousFamilles"
    )

    def __str__(self):
        return self.sousFamille

    class Meta:
        db_table = "sous_famille"


class Marque(models.Model):
    idMarque = models.BigAutoField(primary_key=True)
    marque = models.CharField(max_length=100)

    def __str__(self):
        return self.marque

    class Meta:
        db_table = "marque"


class Model(models.Model):
    idModel = models.BigAutoField(primary_key=True)
    model = models.CharField(max_length=100)
    marque = models.ForeignKey(
        'Marque', on_delete=models.CASCADE, related_name="models"
    )

    def __str__(self):
        return self.model

    class Meta:
        db_table = "model"
