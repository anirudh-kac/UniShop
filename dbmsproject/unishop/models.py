from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# By default, Django gives each model the following field:
# id = models.AutoField(primary_key=True)

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField()
    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="shop")
    image_url = models.URLField(null = True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Shop"

# request.user.profile 
# additional information for predefined model
class UserProfile(models.Model):
    is_employee = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    dob = models.DateField(null=True)
    phone_number = models.PositiveIntegerField()
    address = models.CharField(max_length=100,null= True)
    pincode = models.PositiveIntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "UserProfile"



class Product(models.Model):
    #id added automatically
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image_url = models.URLField(null=True)
    shop = models.ForeignKey('Shop',on_delete=models.CASCADE)

    def __str__(self):
        return self.brand + self.name

    class Meta:
        db_table = "Product"


class CartItem(models.Model):
    product = models.ForeignKey('Product',on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "CartItem"



##bill ~ orders
class Bill(models.Model):
    
    deliver = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    total_price = models.PositiveIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bill")
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE,related_name="bills")

    def __str__(self):
        return self.user.username + "Bill"
    
    class Meta:
        db_table = "Bill"
    

    



