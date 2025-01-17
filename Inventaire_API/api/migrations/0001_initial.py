# Generated by Django 5.1.4 on 2025-01-16 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categorie",
            fields=[
                ("idCategorie", models.BigAutoField(primary_key=True, serialize=False)),
                ("categorie", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "categorie",
            },
        ),
        migrations.CreateModel(
            name="ChampsPersonnalises",
            fields=[
                (
                    "idChampsPersonnales",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("sousCategorie", models.CharField(max_length=100, null=True)),
                ("marque", models.CharField(max_length=100, null=True)),
                ("model", models.CharField(max_length=100, null=True)),
                ("famille", models.CharField(max_length=100, null=True)),
                ("sousFamille", models.CharField(max_length=100, null=True)),
                ("taille", models.CharField(max_length=100, null=True)),
                ("couleur", models.CharField(max_length=100, null=True)),
                ("poids", models.CharField(max_length=100, null=True)),
                ("volume", models.CharField(max_length=100, null=True)),
                ("dimensions", models.CharField(max_length=100, null=True)),
            ],
            options={
                "db_table": "champs_personnalises",
            },
        ),
        migrations.CreateModel(
            name="Depot",
            fields=[
                ("idDepot", models.BigAutoField(primary_key=True, serialize=False)),
                ("depot", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "depot",
            },
        ),
        migrations.CreateModel(
            name="Produit",
            fields=[
                (
                    "reference",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Revente", "Revente"),
                            ("Immobilisation", "Immobilisation"),
                            ("Equipement", "Equipement"),
                        ],
                        max_length=50,
                    ),
                ),
                ("codeBarres", models.CharField(max_length=100)),
                (
                    "uniteType",
                    models.CharField(
                        choices=[("Pièce", "Pièce"), ("Douzaine", "Douzaine")],
                        max_length=50,
                    ),
                ),
                ("prixVenteTTC", models.FloatField()),
                ("description", models.TextField()),
                ("quantite", models.IntegerField()),
                ("codeRFID", models.CharField(blank=True, max_length=100, null=True)),
                ("dateAffectation", models.DateField(blank=True, null=True)),
                ("datePeremption", models.DateField(blank=True, null=True)),
                ("dateCreation", models.DateTimeField(auto_now_add=True)),
                (
                    "categorie",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="produits",
                        to="api.categorie",
                    ),
                ),
                (
                    "champsPersonnalises",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="champsPersonnalises",
                        to="api.champspersonnalises",
                    ),
                ),
                (
                    "depot",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.depot",
                    ),
                ),
            ],
            options={
                "db_table": "produit",
            },
        ),
    ]
