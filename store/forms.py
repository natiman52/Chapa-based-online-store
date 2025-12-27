from rest_framework import serializers
from .models import Cart
class CartSerializer(serializers.ModelSerializer):
    img = serializers.CharField(max_length=225,read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    max_quantity = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cart
        fields = ["id","product","img","quantity","max_quantity"]
        depth = 1
