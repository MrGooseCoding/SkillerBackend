from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import *
from Core.models import *

class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    
    def login(self, request):
        """
            Request params:
                username: str
                password: (private) str

            returns the Account data along with a token
        """
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)

        if user := authenticate(username=username, password=password):
            token = Token.objects.get_or_create(user=user)[0]
            account = Account.objects.get(user=user)
            data = self.serializer_class(account).data
            data['token'] = token.key

            return Response(data)
        
        return Response({"Error":"PasswordNotValid"})

    def retrieve(self, request):
        try:
            token = request.data.get('token')
            return Response(self.serializer_class(Account.objects.get(user=Token.objects.get(key=token).user)).data)
        except:
            return Response({'Error':'TokenNotValid'})
