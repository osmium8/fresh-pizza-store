from rest_framework import serializers
from .models import User
from pizzeria.models import OrderSession

class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Hides 'email' field
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   email=validated_data['email'],
                                   )
        
        user.set_password(validated_data['password'])
        user.save()

        # TODO signal
        session = OrderSession.objects.create(user=user)
        session.save()

        return user
