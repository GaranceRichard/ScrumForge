# backend/certifications/management/commands/seed.py

import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from certifications.models import Certification, Competency, CertificationCompetency

class Command(BaseCommand):
    help = "Seed the database with initial data including certifications and their competencies"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Démarrage du seed...")
        self.apply_migrations()
        self.create_superuser()
        self.create_certifications_and_competencies()
        self.stdout.write("🌱 Seed terminé avec succès !")

    def apply_migrations(self):
        from django.core.management import call_command

        self.stdout.write("🔄 Création des migrations...")
        call_command('makemigrations', interactive=False)
        self.stdout.write("✅ Migrations créées avec succès !")
        
        self.stdout.write("🔄 Application des migrations...")
        call_command('migrate', interactive=False)
        self.stdout.write("✅ Migrations appliquées avec succès !")

    def create_superuser(self):
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

    def create_certifications_and_competencies(self):
        # Définition des certifications avec leurs compétences associées
        certification_data = [
            {
                "name": "Professional Scrum Master I (PSM I)",
                "description": "Compréhension fondamentale de Scrum.",
                "competencies": [
                    {
                        "name": "Fondamentaux de Scrum",
                        "description": "Compréhension claire des rôles, des événements et des artefacts."
                    },
                    {
                        "name": "Empirisme",
                        "description": "Maîtrise des principes de transparence, inspection et adaptation."
                    },
                    {
                        "name": "Facilitation de l’équipe",
                        "description": "Capacité à organiser et animer les réunions Scrum et à gérer les conflits."
                    },
                    {
                        "name": "Culture Scrum",
                        "description": "Intégration des valeurs et de la mentalité agile au sein de l’équipe."
                    },
                ]
            },
            {
                "name": "Professional Scrum Master II (PSM II)",
                "description": "Maîtrise avancée du rôle de Scrum Master.",
                "competencies": [
                    {
                        "name": "Leadership servant avancé",
                        "description": "Coaching et mentorat des équipes dans des contextes complexes."
                    },
                    {
                        "name": "Gestion des environnements difficiles",
                        "description": "Adaptation de Scrum dans des situations variées et inter-équipes."
                    },
                    {
                        "name": "Optimisation des processus",
                        "description": "Identification et mise en œuvre d’améliorations continues pour accroître l’efficacité."
                    },
                    {
                        "name": "Résolution de conflits",
                        "description": "Techniques de médiation et de facilitation pour surmonter les obstacles interpersonnels."
                    },
                ]
            },
            {
                "name": "Professional Scrum Product Owner I (PSPO I)",
                "description": "Fondamentaux du rôle de Product Owner.",
                "competencies": [
                    {
                        "name": "Gestion du Product Backlog",
                        "description": "Priorisation et raffinement des besoins pour maximiser la valeur produit."
                    },
                    {
                        "name": "Vision produit",
                        "description": "Définition et communication d’une vision claire et inspirante."
                    },
                    {
                        "name": "Collaboration avec les parties prenantes",
                        "description": "Coordination efficace entre l’équipe de développement et les clients/utilisateurs."
                    },
                    {
                        "name": "Compréhension économique",
                        "description": "Bases de la création de valeur et gestion des compromis dans le développement produit."
                    },
                ]
            },
            {
                "name": "Professional Scrum Product Owner II (PSPO II)",
                "description": "Gestion avancée du produit.",
                "competencies": [
                    {
                        "name": "Stratégie produit avancée",
                        "description": "Élaboration de stratégies complexes pour optimiser la valeur du produit."
                    },
                    {
                        "name": "Analyse de marché et validation",
                        "description": "Capacité à analyser les besoins du marché et à valider des hypothèses produit."
                    },
                    {
                        "name": "Optimisation du Product Backlog",
                        "description": "Techniques avancées de gestion dans des environnements dynamiques."
                    },
                    {
                        "name": "Leadership transversal",
                        "description": "Coordination avec diverses équipes pour aligner la vision produit avec la réalité terrain."
                    },
                ]
            },
            {
                "name": "Professional Scrum Developer I (PSD I)",
                "description": "Pratiques de développement en Scrum.",
                "competencies": [
                    {
                        "name": "Pratiques de développement agile",
                        "description": "Maîtrise des techniques d’intégration continue, TDD et développement collaboratif."
                    },
                    {
                        "name": "Qualité du code",
                        "description": "Mise en œuvre de pratiques d’ingénierie pour l’excellence technique et la maintenabilité."
                    },
                    {
                        "name": "Collaboration interdisciplinaire",
                        "description": "Travail étroit avec Product Owners et Scrum Masters pour répondre aux besoins du produit."
                    },
                    {
                        "name": "Adaptabilité technologique",
                        "description": "Capacité à intégrer et utiliser des outils modernes facilitant le cycle de développement."
                    },
                ]
            },
            {
                "name": "Scaled Professional Scrum (SPS)",
                "description": "Gestion de Scrum à grande échelle.",
                "competencies": [
                    {
                        "name": "Coordination multi-équipes",
                        "description": "Organisation et synchronisation de plusieurs équipes Scrum sur un produit commun."
                    },
                    {
                        "name": "Gestion des interdépendances",
                        "description": "Identification et résolution des problèmes liés à la coordination à grande échelle."
                    },
                    {
                        "name": "Alignement stratégique",
                        "description": "Mise en place d’objectifs communs et d’une vision partagée dans l’organisation."
                    },
                    {
                        "name": "Optimisation des flux",
                        "description": "Application des principes Scrum pour améliorer l’efficacité globale des processus."
                    },
                ]
            },
            {
                "name": "Professional Agile Leadership I (PAL I)",
                "description": "Soutien du leadership Agile.",
                "competencies": [
                    {
                        "name": "Transformation agile",
                        "description": "Capacité à impulser et accompagner le changement culturel dans l’organisation."
                    },
                    {
                        "name": "Leadership servant",
                        "description": "Application des principes du leadership servant pour favoriser l’autonomie."
                    },
                    {
                        "name": "Gestion du changement",
                        "description": "Techniques de communication et de gestion des résistances au changement."
                    },
                    {
                        "name": "Vision et stratégie agile",
                        "description": "Élaboration de stratégies soutenant la transition vers l’agilité."
                    },
                ]
            },
            {
                "name": "Professional Agile Leadership - Evidence-Based Management (PAL-EBM)",
                "description": "Gestion empirique basée sur les preuves.",
                "competencies": [
                    {
                        "name": "Décision basée sur les données",
                        "description": "Utilisation d’indicateurs et de métriques pour guider les décisions organisationnelles."
                    },
                    {
                        "name": "Mesure de la performance",
                        "description": "Mise en place de systèmes de suivi pour mesurer l’impact des initiatives agiles."
                    },
                    {
                        "name": "Amélioration continue",
                        "description": "Adaptation des stratégies à partir d’analyses empiriques et d’expériences terrain."
                    },
                    {
                        "name": "Culture de la transparence",
                        "description": "Favoriser un environnement de partage des données et des feedbacks."
                    },
                ]
            },
            {
                "name": "Professional Scrum with Kanban I (PSK I)",
                "description": "Intégration des pratiques Kanban dans Scrum.",
                "competencies": [
                    {
                        "name": "Intégration des pratiques Kanban",
                        "description": "Compréhension de la visualisation du flux de travail et limitation du WIP."
                    },
                    {
                        "name": "Optimisation des processus",
                        "description": "Identification des goulots d’étranglement et mise en place d’actions correctives."
                    },
                    {
                        "name": "Amélioration continue",
                        "description": "Application conjointe des principes Scrum et Kanban pour accroître la productivité."
                    },
                    {
                        "name": "Flexibilité opérationnelle",
                        "description": "Capacité à adapter Scrum pour tirer parti des avantages Kanban."
                    },
                ]
            },
            {
                "name": "Professional Scrum with User Experience I (PSU I)",
                "description": "Intégration des pratiques UX dans Scrum.",
                "competencies": [
                    {
                        "name": "Collaboration design-développement",
                        "description": "Intégration des pratiques UX dans le cycle Scrum."
                    },
                    {
                        "name": "Recherche utilisateur",
                        "description": "Conduite d’études qualitatives et quantitatives pour comprendre les besoins utilisateurs."
                    },
                    {
                        "name": "Itération et prototypage",
                        "description": "Utilisation de cycles itératifs pour tester et affiner des hypothèses de design."
                    },
                    {
                        "name": "Expérience client améliorée",
                        "description": "Conception centrée sur l’utilisateur pour maximiser l’ergonomie et la satisfaction."
                    },
                ]
            },
            {
                "name": "Professional Scrum Facilitation Skills (PSFS)",
                "description": "Facilitation efficace en Scrum.",
                "competencies": [
                    {
                        "name": "Techniques de facilitation",
                        "description": "Maîtrise des méthodes pour animer réunions Scrum et ateliers collaboratifs."
                    },
                    {
                        "name": "Gestion des dynamiques de groupe",
                        "description": "Identification et résolution des conflits en favorisant la participation active."
                    },
                    {
                        "name": "Communication efficace",
                        "description": "Techniques pour favoriser écoute, transparence et feedback constructif."
                    },
                    {
                        "name": "Création d’environnements collaboratifs",
                        "description": "Mise en place d’un cadre favorisant l’autonomie et l’innovation."
                    },
                ]
            },
            {
                "name": "Professional Scrum Product Backlog Management Skills (PSPBM)",
                "description": "Gestion efficace du Product Backlog.",
                "competencies": [
                    {
                        "name": "Affinage du Product Backlog",
                        "description": "Techniques avancées de priorisation, découpage et clarification des items."
                    },
                    {
                        "name": "Collaboration avec les parties prenantes",
                        "description": "Coordination étroite pour refléter fidèlement les besoins du marché."
                    },
                    {
                        "name": "Stratégies de gestion de la valeur",
                        "description": "Méthodes pour aligner le backlog sur la vision et les objectifs stratégiques."
                    },
                    {
                        "name": "Utilisation d’outils de gestion agile",
                        "description": "Exploitation d’outils pour optimiser la visibilité et la gestion du backlog."
                    },
                ]
            },
            {
                "name": "Professional Product Discovery and Validation (PPDV)",
                "description": "Techniques de découverte produit.",
                "competencies": [
                    {
                        "name": "Découverte produit",
                        "description": "Méthodologies de recherche et d’identification des opportunités produit basées sur l’expérimentation."
                    },
                    {
                        "name": "Validation d’hypothèses",
                        "description": "Techniques pour tester rapidement des idées et ajuster la stratégie en fonction des retours."
                    },
                    {
                        "name": "Design thinking",
                        "description": "Application des principes de design thinking pour stimuler l’innovation."
                    },
                    {
                        "name": "Itération rapide",
                        "description": "Mise en œuvre de cycles courts de prototypage, test et ajustement."
                    },
                ]
            },
        ]

        # Pour chaque certification, création et association des compétences
        for cert_info in certification_data:
            cert, cert_created = Certification.objects.get_or_create(
                name=cert_info["name"],
                defaults={"description": cert_info["description"]}
            )
            if cert_created:
                self.stdout.write(f"✅ Certification '{cert.name}' créée !")
            else:
                self.stdout.write(f"⚠️ Certification '{cert.name}' existe déjà.")

            for comp_info in cert_info["competencies"]:
                comp, comp_created = Competency.objects.get_or_create(
                    name=comp_info["name"],
                    defaults={"description": comp_info["description"]}
                )
                if comp_created:
                    self.stdout.write(f"✅ Compétence '{comp.name}' créée !")
                else:
                    self.stdout.write(f"⚠️ Compétence '{comp.name}' existe déjà.")

                # Création de l'association entre la certification et la compétence
                assoc, assoc_created = CertificationCompetency.objects.get_or_create(
                    certification=cert,
                    competency=comp
                )
                if assoc_created:
                    self.stdout.write(f"✅ Association entre '{cert.name}' et '{comp.name}' créée !")
                else:
                    self.stdout.write(f"⚠️ Association entre '{cert.name}' et '{comp.name}' existe déjà.")
