import itertools
from django.db import transaction
from ..models.productVariant import ProductVariant
from ..models.ProductOption import ProductOption, VariantOptionValue

def generate_variants_for_product(product):
    
    options = (
        ProductOption.objects.filter(product=product)
        .prefetch_related("values")
    )
    
    #collect option values
    option_values = []
    for option in options:
        values = list(option.values.all())
        if values:
            option_values.append(values)
    
    with transaction.atomic():
        
        if not option_values:
            ProductVariant.objects.create(
                product=product,
                sku=f"{product.id}-DEFAULT",
                price=product.price
            )
            return 
        
        combinations = itertools.product(*option_values)
        
        variant_links = []
        
   
        for combination in combinations:
            
            sku_parts = [v.value for v in combination]
            sku = f"{product.id}-" + '-'.join(sku_parts)
            
            
            variant = ProductVariant.objects.create(
                product=product,
                sku=sku,
                price=product.price
            )
            
            for option_value in combination:
                variant_links.append(
                    VariantOptionValue(
                        variant=variant,
                        option_value=option_value
                    )
                ) 
            
            VariantOptionValue.objects.bulk_create(variant_links)
    