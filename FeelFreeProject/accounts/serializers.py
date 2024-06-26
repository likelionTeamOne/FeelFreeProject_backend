from django.contrib.auth.models import User 
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(write_only=True)

    def create(self, validated_data): 
        name = validated_data.pop('name')
        user = User.objects.create_user(     
            email=validated_data['email'],         
            username = validated_data['username'], 
            password = validated_data['password']   
        )
        user.first_name = name
        user.save()
        return user  
    class Meta:
        model = User
        fields = [ 'username',  'email','password' ,'name'] 