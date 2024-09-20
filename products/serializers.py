from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate_name(self, value):
        
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("Product with the same name already exists")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number")
        return value

    def validate_sale_price(self, value):
        
        price = self.initial_data.get('price')
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("Sale price must be a positive number")
            if price is not None and value >= float(price):
                raise serializers.ValidationError("Sale price must be less than the original price")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value

    def validate(self, data):
        sale_price = data.get('sale_price')
        price = data.get('price')

        if sale_price is not None and price is not None:
            if price <= sale_price:
                raise serializers.ValidationError("Sale price must be less than the regular price")
        return data
