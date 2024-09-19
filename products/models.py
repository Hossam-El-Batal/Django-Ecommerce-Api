from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50,null=False, unique=True)
    price = models.DecimalField(max_digits=100,decimal_places=2,null=False)
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=0)
    sale_price = models.DecimalField(max_digits=99,decimal_places=2,null=True)
    
    
    def __str__(self):
        return self.name

    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price