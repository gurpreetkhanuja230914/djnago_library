from rest_framework import serializers
from .models import MyUser


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        models=MyUser
        fields=['username','password','email','user_type']
        extra_k={'password':{'write-only':True}}
    def create(self,validated_data):
        user=MyUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        return user