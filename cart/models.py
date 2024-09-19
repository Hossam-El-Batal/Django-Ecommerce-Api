from django.db import models
from authentication.models import User
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f'{self.product.name} in {self.user.username}\'s cart'
    
    class Meta:
        unique_together = ('user', 'product') 
