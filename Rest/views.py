from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import *
from .models import Product
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .permissions import ProductPermission, OrderPermission
from django.shortcuts import get_object_or_404


class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ListProductSerializer(queryset, many=True)
        return Response(serializer.data)

    #TO_DO
    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        if ProductPermission.has_permission(request=request):
            Product.objects.create(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                price=serializer.validated_data['price'],
                image=serializer.validated_data['image'],
                tag=serializer.validated_data['tag'],
                owner=serializer.validated_data['owner']
            )
            return Response(status=status.HTTP_201_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class ListOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer


class OrderViewSet(viewsets.ViewSet):

    def list(self, request):
        token_serializer = TokenSerializer(data=request.data, context={'request':request})
        token_serializer.is_valid(raise_exception=True)
        token = Token.objects.get(key=token_serializer.validated_data['token'])
        queryset = Order.objects.filter(user=token.user)
        queryset = [Product.objects.get(name=elem.product) for elem in queryset]
        serializer = ListProductSerializer(queryset, many=True)
        return Response(serializer.data)

    #TO_DO
    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def post(self, request):
        if OrderPermission.has_permission(request=request):
            serializer = OrderSerializer(data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            token_serializer = TokenSerializer(data=request.data, context={'request': request})
            token_serializer.is_valid(raise_exception=True)
            token = Token.objects.get(key=token_serializer.validated_data['token'])
            Order.objects.create(
                user=token.user,
                product=serializer.validated_data['product'],
                is_completed=False
            )
            return Response({'message': 'Ваш заказ успешно оформлен!'})
        return Response("Error 403: Forbidden")
