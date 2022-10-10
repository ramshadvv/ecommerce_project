from django.db import models
from accounts.models import Accounts, CustomerAdress
from productapp.models import Product
import uuid


# Create your models here.


class CartItem(models.Model):
    user = models.ForeignKey(Accounts,on_delete= models.CASCADE, null= True ,blank = True) 
    product = models.ForeignKey(Product,on_delete= models.CASCADE, null= True ,blank = True)
    quantity = models.IntegerField(default=1,null = True ,blank= True)
    size = models.CharField(max_length=50,null = True ,blank= True)
    date_added = models.DateField(auto_now_add=True)
    guest_user  = models.CharField(max_length=200,null=True, blank=True)
    cancel_status = models.BooleanField(default=False, null=True, blank=True)
    reason          = models.CharField(max_length=255,null= True,blank = True)


    def __str__(self):
        return f"{self.quantity} of {self.product}"


    @property
    def get_item_price(self):
        return self.quantity * self.product.get_product_price


STATUS_CHOICES = (
    ("Confirmed" , "Confirmed"),
    ("Shipped" , "Shipped"),
    ("Out for delivery" , "Out for delivery"),
    ("Delivered" , "Delivered"),
    ("Canceled" , "Canceled"),
    ("Returned", "Returned"),

)


class Order(models.Model):
    user            = models.ForeignKey(Accounts,on_delete= models.CASCADE, null = True ,blank = True )
    orderd          = models.BooleanField(default=False)
    Customer        = models.ForeignKey(CustomerAdress,on_delete= models.CASCADE, null = True ,blank = True )
    date_ordered    = models.DateField(auto_now_add= True)
    status          = models.CharField(choices=STATUS_CHOICES,max_length=100,default='Confirmed')
    items           = models.ManyToManyField(CartItem,blank = True )
    transcation_id  = models.UUIDField(default=uuid.uuid4, editable=False,null=True, blank = True)
    payment_method  = models.CharField(max_length=50,null= True,blank = True  )
    total_price     = models.FloatField(null = True ,blank= True)
    date_delivered  = models.DateField(auto_now_add= False,default='2022-01-01')
    guest_user      = models.CharField(max_length=200,null=True, blank=True)
    returnexpiry    = models.BooleanField(default=True,null=True, blank=True)
    reason          = models.CharField(max_length=255,null= True,blank = True)
    discount        = models.CharField(max_length=255,null= True,blank = True, default = "0")
   
    
    def __str__(self):
         return str(self.user)


    @property 
    def total_amount_cart(self):
        total = 0
        for item in self.items.all():
            total += item.get_item_price
        return total


    @property
    def get_tax(self):
        tax = (self.total_amount_cart * 3)/100
        return tax


class MyWishList(models.Model):
    username         = models.ForeignKey(Accounts,on_delete= models.CASCADE, null= True ,blank = True) 
    product     = models.ForeignKey(Product,on_delete= models.CASCADE, null= True ,blank = True)
    def __str__(self):
         return str(self.username)

