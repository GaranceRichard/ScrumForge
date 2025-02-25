#!/usr/bin/env python
"""Utilitaire en ligne de commande pour les tâches administratives de Django."""
import os
import sys

def main():
    """Exécute les tâches administratives."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Assurez-vous qu'il est installé et "
            "disponible sur votre variable d'environnement PYTHONPATH. Avez-vous "
            "oublié d'activer un environnement virtuel ?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
