from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status


#
class RegistrationView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        CustomUser.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        return Response({"message":"Успешно создан новый пользователь!"})


class AuthorizationView(generics.GenericAPIView):
    serializer_class = AuthSerializer

    def post(self, request):
        serializer = AuthSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(username=serializer.validated_data['username'])
        if user.password == serializer.validated_data['password']:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, "message":"Вы успешно авторизовались!"})
        return Response({"Указан неверный пароль"})

class LogOutView(generics.GenericAPIView):
    serializer_class = LogOutSerializer
    def post(self, request):
        serializer = LogOutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        temp = Token.objects.get(key=token)
        if temp.key == token:
            temp.delete()
            return Response({'message':'Succesfully logout'}, status=status.HTTP_200_OK)
        return Response(temp.key, status=status.HTTP_400_BAD_REQUEST)


class ListTokenView(generics.ListAPIView):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()