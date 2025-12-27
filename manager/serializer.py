from rest_framework import serializers
from store.models import Product,Catagory,Image
import json

class ImageSerilizer(serializers.ModelSerializer):
    product_images = serializers.FileField(source="img")
    class Meta:
        model = Image
        fields = ['product','product_images']
class CatagorySerilazer(serializers.ModelSerializer):
    class Meta:
        model =Catagory
        fields = ["name"]
class ProductSerailzer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="name")
    product_about = serializers.CharField(source="about")
    product_price = serializers.CharField(source="price")
    product_detail= serializers.CharField(source="detail")
    product_quantity= serializers.CharField(source="quantity")
    product_weight= serializers.CharField(source="weight")
    product_catagory = serializers.ListField()
    class Meta:
        model = Product
        fields = ["product_name","product_about","product_price","product_detail","product_quantity","product_weight","product_catagory"]
    def create(self,validated_data):
        catagories = self.initial_data['product_catagory']
        cats = [Catagory.objects.get(pk=int(i)) for i in catagories]
        del validated_data["product_catagory"]
        validated_data['detail'] = json.loads(validated_data['detail'] )
        obj = Product.objects.create(**validated_data)
        obj.catagory.set(cats)
        return obj
