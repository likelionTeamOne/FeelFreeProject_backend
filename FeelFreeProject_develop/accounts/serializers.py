from django.contrib.auth.models import User 
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# 회원 가입
class UserSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        # 비밀번호와 비밀번호 확인 확인 로직
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError({'password': '비밀번호와 비밀번호 확인이 일치하지 않습니다. 다시 입력해주세요!'})

        name = validated_data.pop('name')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )

        user.first_name = name
        user.save()
        return user 
    
    class Meta:
        model = User
        fields = ['id','name','username', 'password', 'password_confirm', 'email'] # 피그마에 맞게 순서 수정, 주소 확인 위해 id 필드 추가


# 회원 정보 수정
class UserUpdateSerializer(ModelSerializer) :
    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(write_only=True)
    
    def update(self, instance, validated_data):
        current_password = validated_data.pop('current_password', None)
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)

        # 본인이 맞는지 확인하기 위한 비밀번호 확인 로직
        if current_password and not instance.check_password(current_password):
            raise serializers.ValidationError({'current_password': '현재 비밀번호가 일치하지 않습니다.'})

        # 비밀번호를 정확히 입력했는지 확인하기 위한 로직
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError({'password': '비밀번호와 비밀번호 확인이 일치하지 않습니다. 다시 입력해주세요!'})

        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id','current_password','name','username', 'password', 'password_confirm', 'email'] # 피그마에 맞게 순서 수정