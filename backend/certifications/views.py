from django.http import JsonResponse

def certification_list(request):
    return JsonResponse({"message": "Liste des certifications"})
