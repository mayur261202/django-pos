from .models.product import Product
from .models.category import Category
from rest_framework import serializers
from .models.ProductOption import ProductOption, ProductOptionValue, VariantOptionValue
from .services.variant_service import generate_variants_for_product

class ProductOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = '__all__'

class ProductOptionSerializer(serializers.ModelSerializer):
    values = ProductOptionValueSerializer(many=True)
    
    class Meta:
        model = ProductOption
        fields = '__all__'
        
    def create(self, validated_data):
        values_data = validated_data.pop('values', [])
        option = ProductOption.objects.create(**validated_data)
        ProductOptionValue.objects.bulk_create([
            ProductOptionValue(option=option, value=value['value']) for value in values_data
        ])
        return option
class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(
        many=True,
        required=False,
        write_only=True
    )
    class Meta:
        model = Product
        fields = '__all__'
        
    def create(self, validated_data):
        options_data = validated_data.pop('options')
        
        product = Product.objects.create(**validated_data)
        
        for option_data in options_data:
            option = ProductOption.objects.create(
                product=product,
                name=option_data['name']
            )
            ProductOptionValue.objects.bulk_create([
                ProductOptionValue(option=option, value=value)
                for value in option_data['values']
            ])
        
        generate_variants_for_product(product)

        return product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

        


class VariantOptionValueSerializer(serializers.ModelSerializer):
    
    option_value = ProductOptionValueSerializer(read_only=True)
    option_value_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductOptionValue.objects.all(),
        source='option_value',
        write_only=True
    )
    
    class Meta:
        model = VariantOptionValue
        fields = '__all__'