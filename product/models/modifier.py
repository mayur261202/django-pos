from django.db import models

from .product import Product

class ModifierGroup(models.Model):
    name=models.CharField(max_length=100)
    
    products = models.ManyToManyField(Product, related_name='modifier_groups', blank=True)
    
    def __str__(self):
        return self.name
    
class Modifier(models.Model):
    group = models.ForeignKey(ModifierGroup, related_name='options', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.name