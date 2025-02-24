from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    message = serializers.CharField()
