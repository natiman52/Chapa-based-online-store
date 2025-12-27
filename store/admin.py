from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Catagory)
class cataogryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product',)

@admin.register(StoreDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ("product",)

@admin.register(Discounts)
class Discount(admin.ModelAdmin):
    list_display = ('product',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display= ("product__id",'date')

@admin.register(PaymentLink)
class PaymentLinkAdmin(admin.ModelAdmin):
    list_display = ("txt","link")