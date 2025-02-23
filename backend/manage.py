#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()

    from django.core.management import execute_from_command_line
    import sys

    # ✅ Exécuter le seed automatiquement lors de `migrate` ou `runserver`
    if 'migrate' in sys.argv or 'runserver' in sys.argv:
        seed_path = os.path.join(os.path.dirname(__file__), "seed.py")

        if os.path.exists(seed_path):  # Vérifier si seed.py existe
            import importlib.util
            spec = importlib.util.spec_from_file_location("seed", seed_path)
            seed = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(seed)

            print("🌱 Exécution du script de seed...")
            seed.run()  # Exécuter la fonction `run()` de `seed.py`
        else:
            print("⚠️ `seed.py` introuvable, skipping...")

    execute_from_command_line(sys.argv)