from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class CustomExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        response_data = {"error": "Une erreur interne est survenue."}
        
        if settings.DEBUG:  # En mode dev, afficher les détails
            response_data["details"] = str(exception)

        return JsonResponse(response_data, status=500)
