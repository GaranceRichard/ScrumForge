import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from certifications.models import Certification  # Assurez-vous que c'est bien le bon chemin vers votre modèle

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        """Exécute toutes les fonctions de seed."""
        self.stdout.write("🌱 Démarrage du seed...")
        self.apply_migrations()
        self.create_superuser()
        self.create_certifications()
        self.stdout.write("🌱 Seed terminé avec succès !")

    def apply_migrations(self):
        """Crée et applique les migrations de la base de données."""
        from django.core.management import call_command

        self.stdout.write("🔄 Création des migrations...")
        call_command('makemigrations', interactive=False)
        self.stdout.write("✅ Migrations créées avec succès !")
        
        self.stdout.write("🔄 Application des migrations...")
        call_command('migrate', interactive=False)
        self.stdout.write("✅ Migrations appliquées avec succès !")

    def create_superuser(self):
        """Création du superutilisateur si inexistant"""
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="Admin123!"
            )
            self.stdout.write("✅ Superutilisateur 'admin' créé avec succès !")
        else:
            self.stdout.write("⚠️ Superutilisateur 'admin' existe déjà.")

    def create_certifications(self):
        """Création des certifications Scrum.org"""
        certifications = [
            {"name": "Professional Scrum Master I (PSM I)", "description": "Compréhension fondamentale de Scrum."},
            {"name": "Professional Scrum Master II (PSM II)", "description": "Maîtrise avancée du rôle de Scrum Master."},
            {"name": "Professional Scrum Product Owner I (PSPO I)", "description": "Fondamentaux du rôle de Product Owner."},
            {"name": "Professional Scrum Product Owner II (PSPO II)", "description": "Gestion avancée du produit."},
            {"name": "Professional Scrum Developer I (PSD I)", "description": "Pratiques de développement en Scrum."},
            {"name": "Scaled Professional Scrum (SPS)", "description": "Gestion de Scrum à grande échelle."},
            {"name": "Professional Agile Leadership I (PAL I)", "description": "Soutien du leadership Agile."},
            {"name": "Professional Agile Leadership - Evidence-Based Management (PAL-EBM)", "description": "Gestion empirique basée sur les preuves."},
            {"name": "Professional Scrum with Kanban I (PSK I)", "description": "Intégration des pratiques Kanban dans Scrum."},
            {"name": "Professional Scrum with User Experience I (PSU I)", "description": "Intégration des pratiques UX dans Scrum."},
            {"name": "Professional Scrum Facilitation Skills (PSFS)", "description": "Facilitation efficace en Scrum."},
            {"name": "Professional Scrum Product Backlog Management Skills (PSPBM)", "description": "Gestion efficace du Product Backlog."},
            {"name": "Professional Product Discovery and Validation (PPDV)", "description": "Techniques de découverte produit."}
        ]

        for cert_data in certifications:
            cert, created = Certification.objects.get_or_create(
                name=cert_data["name"],
                defaults={"description": cert_data["description"]}
            )
            if created:
                self.stdout.write(f"✅ Certification '{cert.name}' créée avec succès !")
            else:
                self.stdout.write(f"⚠️ La certification '{cert.name}' existe déjà.")
