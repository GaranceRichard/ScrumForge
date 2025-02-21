from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Nécessite un JWT valide
def home_api(request):
    return Response({"message": "Bienvenue sur l'API !", "user": request.user.username})
