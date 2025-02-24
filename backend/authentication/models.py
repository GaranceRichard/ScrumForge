from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Nous conservons ici uniquement les champs essentiels.
    """
    email = models.EmailField(unique=True)
    
    # Vous pouvez ajouter d'autres champs ici plus tard si nécessaire.
