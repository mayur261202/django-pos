from django.db import models

from .productVariant import ProductVariant
from .product import Product

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=50)
    

class ProductOptionValue(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=50)
    
    
class VariantOptionValue(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    option_value = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("variant", "option_value")
    