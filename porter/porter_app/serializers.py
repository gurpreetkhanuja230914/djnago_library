from rest_framework import serializers
from .models import MyUser,vehicle,categories


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['name','password','email','user_type','adhar_no','bank_account_number']

        extra_kwargs={'password':{'write_only':True}}
    def validate(self, data):
        if data['user_type']=='driver':
            if not data.get('adhar_no') or not data.get('bank_account_number'):
                raise serializers.ValidationError("Driver must provide adhar and bank number")
        # elif data['user_type']=='admin':
        #     raise serializers.ValidationError("admin role can be set by admin only")
        return data
        
    def create(self,validated_data):
        user=MyUser.objects.create_user(
            **validated_data
        )
        return user
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=vehicle
        fields='__all__'
class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=categories
        fields='__all__'