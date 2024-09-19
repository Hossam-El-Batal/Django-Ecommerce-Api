from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer



### using DRF's viewsets for simplicity 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        self.check_admin(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_admin(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_admin(request)
        return super().destroy(request, *args, **kwargs)

    def check_admin(self, request):
        # Check if the user is admin
        if not getattr(request.user, 'isAdmin', False):
            raise PermissionDenied("You do not have permission to perform this action")
    



    