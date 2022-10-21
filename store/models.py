from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,blank = True, null = True)
    name = models.CharField(max_length = 100,null = True, blank = True)
    email = models.CharField(max_length = 100,null = True, blank = True)
    
    def __str__(self):
        return self.name 
    
class Product (models.Model):
    name = models.CharField(max_length = 100,blank = False)
    price = models.FloatField(blank = False)
    digital = models.BooleanField(default = False)
    image = models.ImageField(upload_to = "images/",blank = True)
    
    def __str__(self): 
       return self.name
   

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE,blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    # if complete is False, customer can add new items to box
    complete = models.BooleanField(default = False)
    transaction_id = models.CharField(max_length = 100)
    
    def __str__(self):
        return f'{self.id}' 
     
    
    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    #if customer wants to buy digital product, not physically
    @property 
    def shipping(self):
        shipping = False 
        orderitems = self.orderitem_set.all()   
        for items in orderitems:
            
            if items.product.digital == False:
                shipping = True 
        
        return shipping 
    
#class OrderItem represents Item(s) within our cart
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE, blank = True)
    order = models.ForeignKey(Order,on_delete = models.CASCADE, blank = True)
    quantity = models.IntegerField(default = 0,null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    
  
     
#this class represents shipping address
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE,blank = True)
    order = models.ForeignKey(Order,on_delete = models.CASCADE, blank = True)
    address = models.CharField(max_length = 100,blank = False)
    city = models.CharField(max_length = 100,blank = False)
    state = models.CharField(max_length = 100,blank = False)
    zip_code = models.CharField(max_length = 100,blank = False)
    
    def __str__(self):
        return self.address 
    
    