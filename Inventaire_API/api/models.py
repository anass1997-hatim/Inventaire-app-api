from django.db import models

class Produit(models.Model):
    reference = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=50, choices=[
        ('Revente', 'Revente'),
        ('Immobilisation', 'Immobilisation'),
        ('Equipement', 'Equipement')
    ])
    codeBarres = models.CharField(max_length=100)
    uniteType = models.CharField(max_length=50, choices=[
        ('Pièce', 'Pièce'),
        ('Douzaine', 'Douzaine')
    ])
    prixVenteTTC  = models.FloatField()
    description = models.TextField()
    categorie = models.ForeignKey(
        'Categorie', on_delete=models.CASCADE,
        related_name='produits', null=True
    )
    depot = models.ForeignKey(
        'Depot', null=True , on_delete=models.SET_NULL
    )

    champsPersonnalises = models.ForeignKey (
         'ChampsPersonnalises',  on_delete=models.CASCADE,related_name='champsPersonnalises'
        , null=True
    )
    quantite = models.IntegerField()
    codeRFID = models.CharField(max_length=100, null=True, blank=True)
    dateAffectation = models.DateField(null=True, blank=True)
    datePeremption = models.DateField(null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "produit"


class Categorie(models.Model):
    idCategorie = models.BigAutoField(primary_key=True)
    categorie = models.CharField(max_length=100 )

    def __str__(self):
        return self.categorie

    class Meta:
        db_table = "categorie"


class Depot(models.Model):
    idDepot = models.BigAutoField(primary_key=True)
    depot = models.CharField(max_length=100 )

    def __str__(self):
        return self.depot

    class Meta:
        db_table = "depot"



class ChampsPersonnalises(models.Model):
    idChampsPersonnales = models.BigAutoField(primary_key=True)
    sousCategorie = models.CharField(max_length=100, null=True)
    marque = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    famille = models.CharField(max_length=100, null=True)
    sousFamille = models.CharField(max_length=100, null=True)
    taille = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    poids = models.CharField(max_length=100, null=True)
    volume = models.CharField(max_length=100, null=True)
    dimensions = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "champs_personnalises"
