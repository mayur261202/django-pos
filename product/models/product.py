from django.db import models, transaction

from .category import Category

class Product(models.Model):
    FOOD_TYPES = [('veg', 'Veg'), ('non-veg', 'Non-Veg')]
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPES, default='veg')
    
    base_price= models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    has_variants = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    
        
    
    