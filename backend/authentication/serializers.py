from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password  # 🔹 Import du validateur Django


User = get_user_model()

class HomeSerializer(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    message = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    username = serializers.CharField()
    new_password = serializers.CharField(required=False)  # Seulement si DEBUG=True

class DashboardSerializer(serializers.Serializer):
    message = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_password(self, value):
        """Valide le mot de passe selon les règles Django"""
        try:
            validate_password(value)  # 🔥 Vérifie que le mot de passe respecte les règles de sécurité
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)  # 🔹 Retourne les erreurs sous forme de liste
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
