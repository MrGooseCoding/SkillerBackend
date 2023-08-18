from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import *
from Core.models import *
from re import fullmatch

class UserSerializer(ModelSerializer):
    username = CharField(required=True, max_length=150)
    first_name = CharField(required=True, min_length=1, max_length=150)
    password = CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'date_joined', 'password')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.fist_name)
        instance.save()
        return instance
    
    def validate_username(self, username):
        """
            Called after the is_valid function to validate the username
        """
        username_regex = r'^[0-9a-zA-Z1-9._+]+$'

        if User.objects.filter(username=username.lower()).exists():
            raise ValidationError(f'User\'s username has to be unique')

        if not fullmatch(username_regex, username):
            raise ValidationError(f'User\'s username can only include numbers, leters and . _ + symbols')
        
        else:
            return username.lower()

class AccountSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Account
        fields = ('__all__')

    def create(self, validated_data):
        return Account(**validated_data) 