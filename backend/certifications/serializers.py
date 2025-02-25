from rest_framework import serializers
from .models import Certification, Competency

class CompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Competency
        fields = ['id', 'name', 'description']

# backend/certifications/serializers.py

class CertificationSerializer(serializers.ModelSerializer):
    competencies = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = ['id', 'name', 'description', 'logo', 'competencies']

    def get_competencies(self, obj) -> list:
        # Récupère les compétences via la relation CertificationCompetency
        competency_list = [cc.competency for cc in obj.certificationcompetency_set.all()]
        return CompetencySerializer(competency_list, many=True).data

# backend/certifications/serializers.py (ou dans un module dédié)
from rest_framework import serializers

class CertificationCompetencyUpdateSerializer(serializers.Serializer):
    competency_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        required=True,
        help_text="Liste des IDs des compétences à associer"
    )

