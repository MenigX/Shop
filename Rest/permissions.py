from rest_framework import permissions
from .serializers import TokenSerializer
from rest_framework.authtoken.models import Token

class ProductPermission():
    @staticmethod
    def has_permission(request):
        if request.method in permissions.SAFE_METHODS:
            return True
        serializer = TokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token = Token.objects.get(key=serializer.validated_data['token'])
        if token.user.role == 's':
            if token.user != serializer.validated_data['owner']:
                return False
            return True
        else:
            return False
        


class OrderPermission():
    @staticmethod
    def has_permission(request):
        serializer = TokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token = Token.objects.get(key=serializer.validated_data['token'])
        if token.user.role == 'b':
            return True
        else:
            return False