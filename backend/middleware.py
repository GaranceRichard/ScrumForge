from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class CustomExceptionMiddleware(MiddlewareMixin):
    """Middleware pour capturer et formater les erreurs en JSON"""

    def process_exception(self, request, exception):
        response_data = {
            "error": "Une erreur interne est survenue.",
            "details": str(exception)  # Optionnel, utile en dev
        }
        return JsonResponse(response_data, status=500)
