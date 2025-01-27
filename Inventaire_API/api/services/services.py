from django.db.models import Q

from ..models import Produit


def search_product_suggestions(query, limit=10):
    query = query.strip().lower()

    if not query:
        return []

    suggestions = Produit.objects.filter(
        Q(reference__icontains=query) |
        Q(description__icontains=query) |
        Q(codeBarres__icontains=query) |
        Q(categorie__categorie__icontains=query) |
        Q(champsPersonnalises__sousCategorie__sousCategorie__icontains=query) |
        Q(champsPersonnalises__marque__marque__icontains=query) |
        Q(champsPersonnalises__model__model__icontains=query)
    ).select_related(
        'categorie',
        'champsPersonnalises',
        'type',
        'uniteType'
    ).distinct()[:limit]

    product_suggestions = []
    for product in suggestions:
        suggestion = {
            'reference': product.reference,
            'description': product.description,
            'price': product.prixVenteTTC,
            'category': product.categorie.categorie if product.categorie else None,
            'brand': product.champsPersonnalises.marque.marque if product.champsPersonnalises and product.champsPersonnalises.marque else None,
            'model': product.champsPersonnalises.model.model if product.champsPersonnalises and product.champsPersonnalises.model else None,
            'type': product.type.nom if product.type else None,
            'unit_type': product.uniteType.nom if product.uniteType else None
        }
        product_suggestions.append(suggestion)

    return product_suggestions