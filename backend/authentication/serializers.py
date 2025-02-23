from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password  # 🔹 Import du validateur Django

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)  # 🔹 Assure un min de 8 caractères

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
