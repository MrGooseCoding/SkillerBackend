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

    def create(self, request):
        username = request.data.get('username', '')
        first_name = request.data.get('first_name', '')
        password = request.data.get('password', '')

        user_serializer = UserSerializer(data={
            "username":username.strip(),
            "first_name":first_name.strip(),
            "password":password,
        })

        if not user_serializer.is_valid():
            return Response(user_serializer.errors)
        
        user = User(**user_serializer.data)
        user.save()
        account = Account(user=user)
        account.save()

        token= Token.objects.create(user=user).key

        response = {
            **self.serializer_class(account).data,
            'token':token
        }

        return Response(response)
    
    def login(self, request):
        """
            Request params:
                username: str
                password: (private) str

            returns the Account data along with a token
        """
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        print(username, password)

        response = {}

        if user := authenticate(username=username, password=password):
            token = Token.objects.get_or_create(user=user)[0]
            account = Account.objects.get(user=user)
            data = self.serializer_class(account).data
            data['token'] = token.key

            return Response(data)
        
        if not User.objects.filter(username=username.lower()).exists():
            response['username'] = ["Username does not exist"]
        
        if len(password) < 8:
            response['password'] = ["Ensure this field has at least 8 characters."]

        return Response(response)

    def retrieve(self, request):
        try:
            token = request.data.get('token')
            return Response(self.serializer_class(Account.objects.get(user=Token.objects.get(key=token).user)).data)
        except:
            return Response({'Error':'TokenNotValid'})
        
    def search(self, request):        
        username = request.data.get('username', '')      
        try:
            token = Token.objects.get(key=request.data.get('token', ''))
            user =  User.objects.filter(username=username.lower())
            if not user.exists():
                response={}
                response['username'] = ["Username does not exist"]
                return Response(response)
            return Response(self.serializer_class(Account.objects.get(user__username=username.lower())).data) 
        except Exception as e:
          #  print(e)
            return Response({'Error':'TokenNotValid'})
    