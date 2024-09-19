from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer



### overriding  DRF's viewsets to check if isAdmin is set to true ( simple admin check ) 

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
    
    def list(self, request, *args, **kwargs):
        self.check_admin(request)
        return super().list(request, *args, **kwargs)
    
    def check_admin(self, request):
        if not getattr(request.user, 'isAdmin', False):
            raise PermissionDenied("You do not have permission to perform this action")
    



    