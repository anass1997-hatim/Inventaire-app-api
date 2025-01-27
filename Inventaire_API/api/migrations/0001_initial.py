# Generated by Django 5.1.4 on 2025-01-25 21:21

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
            name="Famille",
            fields=[
                ("idFamille", models.BigAutoField(primary_key=True, serialize=False)),
                ("famille", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "famille",
            },
        ),
        migrations.CreateModel(
            name="Marque",
            fields=[
                ("idMarque", models.BigAutoField(primary_key=True, serialize=False)),
                ("marque", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "marque",
            },
        ),
        migrations.CreateModel(
            name="TagTid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tid",
                    models.CharField(
                        help_text="Tag Identifier (unique and immutable)",
                        max_length=128,
                        unique=True,
                    ),
                ),
                (
                    "epc",
                    models.CharField(
                        help_text="Electronic Product Code (programmable)",
                        max_length=128,
                        unique=True,
                    ),
                ),
                (
                    "user",
                    models.TextField(
                        blank=True,
                        help_text="Optional user-defined data stored in the tag",
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "tagTid",
            },
        ),
        migrations.CreateModel(
            name="TypeProduit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "db_table": "type_produit",
            },
        ),
        migrations.CreateModel(
            name="UniteType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "db_table": "unite_type",
            },
        ),
        migrations.CreateModel(
            name="Model",
            fields=[
                ("idModel", models.BigAutoField(primary_key=True, serialize=False)),
                ("model", models.CharField(max_length=100)),
                (
                    "marque",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="models",
                        to="api.marque",
                    ),
                ),
            ],
            options={
                "db_table": "model",
            },
        ),
        migrations.CreateModel(
            name="SousCategorie",
            fields=[
                (
                    "idSousCategorie",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("sousCategorie", models.CharField(max_length=100)),
                (
                    "categorie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sousCategories",
                        to="api.categorie",
                    ),
                ),
            ],
            options={
                "db_table": "sous_categorie",
            },
        ),
        migrations.CreateModel(
            name="SousFamille",
            fields=[
                (
                    "idSousFamille",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("sousFamille", models.CharField(max_length=100)),
                (
                    "famille",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sousFamilles",
                        to="api.famille",
                    ),
                ),
            ],
            options={
                "db_table": "sous_famille",
            },
        ),
        migrations.CreateModel(
            name="ChampsPersonnalises",
            fields=[
                (
                    "idChampsPersonnalises",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("taille", models.CharField(max_length=100, null=True)),
                ("couleur", models.CharField(max_length=100, null=True)),
                ("poids", models.CharField(max_length=100, null=True)),
                ("volume", models.CharField(max_length=100, null=True)),
                ("dimensions", models.CharField(max_length=100, null=True)),
                (
                    "famille",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="champs",
                        to="api.famille",
                    ),
                ),
                (
                    "marque",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="champs",
                        to="api.marque",
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="champs",
                        to="api.model",
                    ),
                ),
                (
                    "sousCategorie",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="champs",
                        to="api.souscategorie",
                    ),
                ),
                (
                    "sousFamille",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="champs",
                        to="api.sousfamille",
                    ),
                ),
            ],
            options={
                "db_table": "champs_personnalises",
            },
        ),
        migrations.CreateModel(
            name="Produit",
            fields=[
                (
                    "reference",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("codeBarres", models.CharField(max_length=100)),
                ("prixVenteTTC", models.FloatField()),
                ("description", models.TextField()),
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
                        related_name="produits",
                        to="api.champspersonnalises",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="produits",
                        to="api.typeproduit",
                    ),
                ),
                (
                    "uniteType",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="produits",
                        to="api.unitetype",
                    ),
                ),
            ],
            options={
                "db_table": "produit",
            },
        ),
    ]
