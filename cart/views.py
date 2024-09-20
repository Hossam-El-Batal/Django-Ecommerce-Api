from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, Product
from .serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        if not self.is_authenticated():
            return Cart.objects.none()  
        return Cart.objects.filter(user=self.request.user)

    def is_authenticated(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return False
        return True

   
    def create(self, request, *args, **kwargs):
        if not self.is_authenticated():
            return Response({"detail": "Authentication is required"}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id:
            return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not quantity or quantity < 1:
            return Response({"detail": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        available_quantity = product.quantity 
        if quantity > available_quantity:
            quantity = available_quantity
   
        existing_cart_item = Cart.objects.filter(user=self.request.user, product=product).first()

        if existing_cart_item:
       
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
            serializer = self.get_serializer(existing_cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

   
        cart_item = Cart.objects.create(user=self.request.user, product=product, quantity=quantity)
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not self.is_authenticated():
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is not None:
            if quantity < 1:
                return Response({"detail": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)
            instance.quantity = quantity  
            
            available_quantity = instance.product.quantity
            if quantity > available_quantity:
                quantity = available_quantity  

            instance.quantity = quantity
            
        self.perform_update(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, *args, **kwargs):

        if not self.is_authenticated():
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        
        instance.delete()

    @action(detail=False, methods=['get'])
    def view_cart(self, *args, **kwargs):
        if not self.is_authenticated():
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        cart_items = self.get_queryset()
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['get'])
    def cart_total(self, request):
        user_cart_items = Cart.objects.filter(user=request.user)
        subtotal = 0
        for item in user_cart_items:
            product = item.product
            price = float(product.sale_price) if product.sale_price else float(product.price)
            subtotal += price * item.quantity
    

        subtotal = round(subtotal, 2)
        total = subtotal 

        return Response({
            "subtotal": subtotal,
            "total": total
    })
