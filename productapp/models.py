from django.db import models
from accounts.models import Accounts


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    category_offer = models.IntegerField(null = True,blank=True,default=0)


    def __str__(self):
        return self.category_name

    class meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_name    = models.CharField(max_length=100)
    description     = models.TextField(max_length=2000, null=True)
    price           = models.IntegerField(null=True)
    stock           = models.IntegerField(null=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    brand           = models.CharField(max_length=100, null=True, blank=True)    
    product_offer   = models.IntegerField(null = True,blank=True,default=0)
    image           = models.ImageField(null= True,blank = True,upload_to ='images/')
    image1          = models.ImageField(null= True,blank = True,upload_to ='images/')
    image2          = models.ImageField(null= True,blank = True,upload_to ='images/')
    product_status  = models.BooleanField(default=True)


    def __str__(self):
        return self.product_name


    class meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    @property
    def get_product_price(self):
        if self.product_offer == 0 and self.category.category_offer==0:
            product_price = self.price
        elif self.product_offer < self.category.category_offer:
            product_price = self.price - float((self.price * self.category.category_offer)/100)
        else:
            product_price = self.price - float((self.price * self.product_offer)/100)
        product_price = float(product_price)
        return product_price

        
class Coupen(models.Model):
    coupencode   = models.CharField( max_length=20, null = True,blank = True)
    coupen_offer = models.IntegerField(null = True,blank=True,default=0)
    is_active    = models.BooleanField(null=True, blank=True, default=True)
    expiry_date  = models.DateField(null=True, blank=True)
    users        = models.ManyToManyField(Accounts, blank=True)
    
    
    def __str__(self):
        return str(self.coupencode)


@property
def get_coupen_offer_price(self):
    coupen_price = self.price - self.coupen_offer
    return coupen_price

