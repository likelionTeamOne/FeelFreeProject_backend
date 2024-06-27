from django.contrib.auth.models import User 
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # 비밀번호화, 비밀번호 확인 추가
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        
        # 비밀번호 확인 로직
        if password != password_confirm:
            raise serializers.ValidationError({'password': '비밀번호와 비밀번호 확인이 일치하지 않습니다.'})

        name = validated_data.pop('name')
        user = User.objects.create_user(     
            email=validated_data['email'],         
            username = validated_data['username'], 
            password = password
        )
        user.first_name = validated_data['name']
        user.save()
        return user 

    # 회원 정보 수정
    def update(self, instance, validated_data):
    # 비밀번호 확인 로직
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError({'password': '비밀번호와 비밀번호 확인이 일치하지 않습니다.'})

        if password and password_confirm:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


    class Meta:
        model = User
        fields = ['name','username', 'password', 'password_confirm', 'email'] # 피그마에 맞게 순서 수정