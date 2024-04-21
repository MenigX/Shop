from rest_framework import serializers
from .models import Product, Order


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'product')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('user', )


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)