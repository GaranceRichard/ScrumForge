from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_login']

class UserSelfUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class UserAdminUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class UserDeleteResponseSerializer(serializers.Serializer):
    message = serializers.CharField()