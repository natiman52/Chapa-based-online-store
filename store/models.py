from django.db import models
from users.models import User
import os
from django.utils import timezone
# Create your models here.

def uploadto(ins,filename):
    path =os.path.join("products",ins.product.name,filename)
    return path

class Catagory(models.Model):
    name = models.CharField(max_length=225)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=225)
    detail = models.JSONField(blank=True,null=True)
    about = models.TextField(blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    views = models.ManyToManyField(User)
    weight = models.IntegerField(default=2)
    promoted= models.BooleanField(default=False)
    catagory = models.ManyToManyField(Catagory,related_name="catagory",null=True,blank=True)
    date = models.DateField(default=timezone.datetime.today)
    def __str__(self):
        return self.name
class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="rated")
    product= models.ForeignKey(Product,on_delete=models.CASCADE,related_name="rating")
    rate = models.IntegerField()
class Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    img = models.ImageField(upload_to=uploadto)
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="added_cart")

class Discounts(models.Model):
    txt = models.CharField(max_length=225)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    discount = models.IntegerField()
    def __str__(self):
        return self.txt
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="history")
    product =models.ForeignKey(Product,on_delete=models.CASCADE,related_name="boughted_by")
    quantity =models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=225,default="pending",choices=(("pending","pending"),('failed',"failed"),("success","success")))
    date = models.DateField(default=timezone.datetime.today)
    link = models.CharField(max_length=225,blank=True,null=True)
    delivery_on = models.BooleanField(default=False)
    deliveried = models.BooleanField(default=False)

class PaymentLink(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.CharField(max_length=225)
    txt = models.CharField(max_length=225)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.datetime.today)
class StoreDiscount(models.Model):
    img = models.ImageField(upload_to="deals/")
    discount = models.FloatField()
    txt = models.CharField(max_length=225)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.product.name