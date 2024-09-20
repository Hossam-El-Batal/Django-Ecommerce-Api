from rest_framework import serializers
from .models import Cart, Product

class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)  
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_id', 'quantity'] 

    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'price': obj.product.price,
            'sale_price': float(obj.product.sale_price) if obj.product.sale_price else None
        }

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product with this ID does not exist")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        
        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
        else:
            cart_item.quantity = validated_data.get('quantity', 1)
        
        cart_item.save()
        return cart_item
