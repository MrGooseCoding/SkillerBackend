from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import *
from Core.models import *

class UserSerializer(ModelSerializer):
    username = CharField(required=True, max_length=150)
    first_name = CharField(required=True, min_length=1, max_length=150)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'date_joined')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.fist_name)
        instance.save()
        return instance

class AccountSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Account
        fields = ('__all__')

    def create(self, validated_data):
        return Account(**validated_data) 