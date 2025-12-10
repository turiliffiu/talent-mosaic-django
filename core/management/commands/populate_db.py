"""
Management command per popolare il database con dati di esempio realistici
Uso: python manage.py populate_db [--flush]

VERSIONE 2.0 - Include Projects e Analytics
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from accounts.models import UserProfile
from skills.models import Skill, SkillCategory, UserSkill
from events.models import Event, EventRegistration
from mentorship.models import Mentorship, MentorshipSession
from challenges.models import Challenge, ChallengeParticipation
from badges.models import Badge, UserBadge
from projects.models import (
    Project, ProjectRequiredSkill, ProjectRole, TeamMember, 
    AIMatchingRun, AdminAction
)
from analytics.models import ActivityLog


class Command(BaseCommand):
    help = 'Popola il database con dati di esempio per demo (include Projects e Analytics)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Elimina tutti i dati esistenti prima di popolare',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎯 TALENT MOSAIC - Popolamento Database Demo v2.0'))
        self.stdout.write('=' * 70)
        
        if options['flush']:
            self.stdout.write(self.style.WARNING('\n⚠️  Eliminazione dati esistenti...'))
            self.flush_data()
        
        self.stdout.write(self.style.SUCCESS('\n📊 Inizio creazione dati di esempio...\n'))
        
        # Ordine di creazione
        self.create_skill_categories()
        self.create_skills()
        self.create_users()
        self.create_user_skills()
        self.create_badges()
        self.create_user_badges()
        self.create_events()
        self.create_event_registrations()
        self.create_mentorships()
        self.create_mentorship_sessions()
        self.create_challenges()
        self.create_challenge_participations()
        
        # NUOVE SEZIONI
        self.create_projects()
        self.create_project_skills()
        self.create_project_roles()
        self.create_team_members()
        self.create_ai_matching_runs()
        self.create_admin_actions()
        self.create_analytics_data()
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('✅ Popolamento completato con successo!'))
        self.print_summary()

    def flush_data(self):
        """Elimina tutti i dati (esclusi superuser)"""
        # Analytics
        ActivityLog.objects.all().delete()
        
        # Projects
        AdminAction.objects.all().delete()
        AIMatchingRun.objects.all().delete()
        TeamMember.objects.all().delete()
        ProjectRole.objects.all().delete()
        ProjectRequiredSkill.objects.all().delete()
        Project.objects.all().delete()
        
        # Existing data
        UserBadge.objects.all().delete()
        Badge.objects.all().delete()
        ChallengeParticipation.objects.all().delete()
        Challenge.objects.all().delete()
        MentorshipSession.objects.all().delete()
        Mentorship.objects.all().delete()
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        UserSkill.objects.all().delete()
        Skill.objects.all().delete()
        SkillCategory.objects.all().delete()
        
        # Elimina utenti non-superuser
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('  ✓ Dati eliminati'))

    def create_skill_categories(self):
        """Crea categorie di competenze"""
        self.stdout.write('📁 Categorie Competenze...')
        
        categories_data = [
            {'name': 'Programmazione', 'icon': 'fa-code', 'color': '#3B82F6', 'order': 1},
            {'name': 'Design & Creatività', 'icon': 'fa-palette', 'color': '#EC4899', 'order': 2},
            {'name': 'Marketing & Comunicazione', 'icon': 'fa-bullhorn', 'color': '#10B981', 'order': 3},
            {'name': 'Management & Leadership', 'icon': 'fa-briefcase', 'color': '#F59E0B', 'order': 4},
            {'name': 'Data & Analytics', 'icon': 'fa-chart-line', 'color': '#8B5CF6', 'order': 5},
            {'name': 'Soft Skills', 'icon': 'fa-users', 'color': '#06B6D4', 'order': 6},
        ]
        
        for cat_data in categories_data:
            cat, created = SkillCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'display_order': cat_data['order'],
                    'description': f'Competenze relative a {cat_data["name"].lower()}'
                }
            )
            if created:
                self.stdout.write(f'  ✓ {cat.name}')

    def create_skills(self):
        """Crea competenze specifiche"""
        self.stdout.write('🧠 Competenze...')
        
        skills_data = {
            'Programmazione': [
                'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'Go', 'Rust',
                'Django', 'React', 'Vue.js', 'Node.js', 'FastAPI', 'Spring Boot',
                'SQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
                'Git', 'CI/CD', 'AWS', 'Azure', 'Google Cloud'
            ],
            'Design & Creatività': [
                'UI/UX Design', 'Adobe Photoshop', 'Adobe Illustrator', 'Figma',
                'Sketch', 'Graphic Design', 'Video Editing', 'Animation',
                'Branding', 'Typography', 'Color Theory'
            ],
            'Marketing & Comunicazione': [
                'SEO', 'SEM', 'Content Marketing', 'Social Media Marketing',
                'Email Marketing', 'Copywriting', 'Public Relations',
                'Brand Management', 'Digital Strategy', 'Analytics'
            ],
            'Management & Leadership': [
                'Project Management', 'Team Leadership', 'Agile', 'Scrum',
                'Strategic Planning', 'Budget Management', 'Stakeholder Management',
                'Change Management', 'Risk Management', 'People Management'
            ],
            'Data & Analytics': [
                'Data Analysis', 'Machine Learning', 'Deep Learning', 'Statistics',
                'Python for Data Science', 'R', 'Tableau', 'Power BI', 'Excel',
                'SQL for Analytics', 'Big Data', 'Data Visualization'
            ],
            'Soft Skills': [
                'Public Speaking', 'Negoziazione', 'Problem Solving', 'Critical Thinking',
                'Creatività', 'Empatia', 'Teamwork', 'Time Management',
                'Adaptability', 'Conflict Resolution', 'Mentoring', 'Coaching'
            ],
        }
        
        count = 0
        for cat_name, skills_list in skills_data.items():
            category = SkillCategory.objects.get(name=cat_name)
            for skill_name in skills_list:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    defaults={
                        'category': category,
                        'is_active': True,
                        'description': f'Competenza in {skill_name}'
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} competenze create')

    def create_users(self):
        """Crea utenti di esempio con profili completi"""
        self.stdout.write('👤 Utenti e Profili...')
        
        users_data = [
            {
                'username': 'mario.rossi',
                'first_name': 'Mario',
                'last_name': 'Rossi',
                'email': 'mario.rossi@fibercop.it',
                'is_staff': True,  # Admin
                'profile': {
                    'job_title': 'Senior Software Engineer',
                    'department': 'IT Development',
                    'bio': 'Appassionato di tecnologia con 10 anni di esperienza nello sviluppo software.',
                    'location': 'Milano, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'giulia.bianchi',
                'first_name': 'Giulia',
                'last_name': 'Bianchi',
                'email': 'giulia.bianchi@fibercop.it',
                'profile': {
                    'job_title': 'UX/UI Designer',
                    'department': 'Design',
                    'bio': 'Designer con passione per user experience e accessibilità.',
                    'location': 'Roma, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'luca.verdi',
                'first_name': 'Luca',
                'last_name': 'Verdi',
                'email': 'luca.verdi@fibercop.it',
                'profile': {
                    'job_title': 'Junior Developer',
                    'department': 'IT Development',
                    'bio': 'Giovane sviluppatore entusiasta di imparare nuove tecnologie.',
                    'location': 'Milano, Italia',
                    'is_mentor': False,
                    'is_mentee': True,
                }
            },
            {
                'username': 'anna.neri',
                'first_name': 'Anna',
                'last_name': 'Neri',
                'email': 'anna.neri@fibercop.it',
                'is_staff': True,  # Admin
                'profile': {
                    'job_title': 'Marketing Manager',
                    'department': 'Marketing',
                    'bio': 'Esperta in digital marketing e social media strategy.',
                    'location': 'Torino, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'marco.ricci',
                'first_name': 'Marco',
                'last_name': 'Ricci',
                'email': 'marco.ricci@fibercop.it',
                'profile': {
                    'job_title': 'Data Analyst',
                    'department': 'Data Science',
                    'bio': 'Analista dati con forte interesse per machine learning.',
                    'location': 'Bologna, Italia',
                    'is_mentor': False,
                    'is_mentee': True,
                }
            },
            {
                'username': 'sara.ferrari',
                'first_name': 'Sara',
                'last_name': 'Ferrari',
                'email': 'sara.ferrari@fibercop.it',
                'profile': {
                    'job_title': 'Project Manager',
                    'department': 'Operations',
                    'bio': 'Project manager con certificazione PMP e esperienza in Agile.',
                    'location': 'Napoli, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'francesco.russo',
                'first_name': 'Francesco',
                'last_name': 'Russo',
                'email': 'francesco.russo@fibercop.it',
                'profile': {
                    'job_title': 'Data Scientist',
                    'department': 'Data Science',
                    'bio': 'Data scientist specializzato in deep learning e NLP.',
                    'location': 'Milano, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'elena.conti',
                'first_name': 'Elena',
                'last_name': 'Conti',
                'email': 'elena.conti@fibercop.it',
                'profile': {
                    'job_title': 'Content Creator',
                    'department': 'Marketing',
                    'bio': 'Content creator con passione per storytelling e video.',
                    'location': 'Roma, Italia',
                    'is_mentor': False,
                    'is_mentee': True,
                }
            },
            {
                'username': 'alessandro.bruno',
                'first_name': 'Alessandro',
                'last_name': 'Bruno',
                'email': 'alessandro.bruno@fibercop.it',
                'profile': {
                    'job_title': 'DevOps Engineer',
                    'department': 'IT Operations',
                    'bio': 'DevOps engineer con expertise in containerizzazione e cloud.',
                    'location': 'Firenze, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'chiara.moretti',
                'first_name': 'Chiara',
                'last_name': 'Moretti',
                'email': 'chiara.moretti@fibercop.it',
                'profile': {
                    'job_title': 'Backend Developer',
                    'department': 'IT Development',
                    'bio': 'Backend developer specializzata in API design e microservizi.',
                    'location': 'Genova, Italia',
                    'is_mentor': False,
                    'is_mentee': True,
                }
            },
        ]
        
        count = 0
        for user_data in users_data:
            profile_data = user_data.pop('profile')
            is_staff = user_data.pop('is_staff', False)
            
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    **user_data,
                    'is_staff': is_staff,
                }
            )
            
            if created:
                user.set_password('demo123')
                user.save()
                count += 1
            
            # Crea o aggiorna UserProfile (get_or_create invece di create)
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults=profile_data
            )
            
            # Se il profilo esiste già, aggiorna i campi
            if not profile_created:
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()
        
        self.stdout.write(f'  ✓ {count} utenti creati (password: demo123)')

    def create_user_skills(self):
        """Assegna competenze agli utenti"""
        self.stdout.write('🎯 Competenze Utente...')
        
        user_skills_mapping = {
            'mario.rossi': ['Python', 'Django', 'JavaScript', 'React', 'Docker', 'Git', 'PostgreSQL'],
            'giulia.bianchi': ['UI/UX Design', 'Figma', 'Adobe Illustrator', 'Graphic Design', 'Branding'],
            'luca.verdi': ['Python', 'JavaScript', 'Git', 'SQL'],
            'anna.neri': ['Content Marketing', 'SEO', 'Social Media Marketing', 'Copywriting', 'Digital Strategy'],
            'marco.ricci': ['Python for Data Science', 'SQL for Analytics', 'Excel', 'Tableau', 'Data Analysis'],
            'sara.ferrari': ['Project Management', 'Agile', 'Scrum', 'Team Leadership', 'Risk Management'],
            'francesco.russo': ['Machine Learning', 'Deep Learning', 'Python', 'Statistics', 'Data Visualization'],
            'elena.conti': ['Content Marketing', 'Video Editing', 'Social Media Marketing', 'Copywriting'],
            'alessandro.bruno': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Git', 'Python'],
            'chiara.moretti': ['Python', 'Django', 'FastAPI', 'PostgreSQL', 'MongoDB', 'Git'],
        }
        
        count = 0
        for username, skill_names in user_skills_mapping.items():
            try:
                user = User.objects.get(username=username)
                for skill_name in skill_names:
                    try:
                        skill = Skill.objects.get(name=skill_name)
                        proficiency = random.randint(3, 5)
                        
                        user_skill, created = UserSkill.objects.get_or_create(
                            user=user,
                            skill=skill,
                            defaults={
                                'proficiency': proficiency,
                                'years_experience': random.randint(1, 10),
                                'verified': random.choice([True, True, False]),
                            }
                        )
                        if created:
                            count += 1
                    except Skill.DoesNotExist:
                        pass
            except User.DoesNotExist:
                pass
        
        self.stdout.write(f'  ✓ {count} competenze-utente create')

    def create_badges(self):
        """Crea badge di achievement"""
        self.stdout.write('🏅 Badge...')
        
        badges_data = [
            {
                'name': 'Mentor Expert',
                'description': 'Ha guidato con successo 5+ mentee',
                'icon': 'badges/mentor_expert.png',  # Path fittizio
                'color': '#10B981',
                'rarity': 'rare',
                'points': 100,
                'criteria': {'mentees_count': 5},
                'auto_award': True,
            },
            {
                'name': 'Skill Master',
                'description': 'Ha acquisito 10+ competenze verificate',
                'icon': 'badges/skill_master.png',
                'color': '#3B82F6',
                'rarity': 'epic',
                'points': 150,
                'criteria': {'verified_skills': 10},
                'auto_award': True,
            },
            {
                'name': 'Team Player',
                'description': 'Ha collaborato a 5+ progetti di squadra',
                'icon': 'badges/team_player.png',
                'color': '#8B5CF6',
                'rarity': 'uncommon',
                'points': 75,
                'criteria': {'projects_count': 5},
                'auto_award': False,
            },
            {
                'name': 'Innovation Champion',
                'description': 'Ha vinto una challenge aziendale',
                'icon': 'badges/innovation_champion.png',
                'color': '#F59E0B',
                'rarity': 'legendary',
                'points': 200,
                'criteria': {'challenge_wins': 1},
                'auto_award': False,
            },
            {
                'name': 'Event Enthusiast',
                'description': 'Ha partecipato a 10+ eventi',
                'icon': 'badges/event_enthusiast.png',
                'color': '#EC4899',
                'rarity': 'common',
                'points': 50,
                'criteria': {'events_attended': 10},
                'auto_award': True,
            },
        ]
        
        count = 0
        for badge_data in badges_data:
            # Rimuovi 'icon' dai defaults se il campo è ImageField vuoto
            icon_path = badge_data.pop('icon', None)
            
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults={
                    **badge_data,
                    # Lascia icon vuoto, verrà popolato dopo se necessario
                }
            )
            if created:
                count += 1
        
        self.stdout.write(f'  ✓ {count} badge creati')

    def create_user_badges(self):
        """Assegna badge agli utenti"""
        self.stdout.write('🎖️  Assegnazione Badge...')
        
        users = User.objects.filter(is_superuser=False)
        badges = Badge.objects.all()
        
        count = 0
        for user in users:
            # Ogni utente ha 1-3 badge casuali
            num_badges = random.randint(1, 3)
            user_badges = random.sample(list(badges), min(num_badges, len(badges)))
            
            for badge in user_badges:
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=badge,
                    defaults={
                        'notes': f'Badge assegnato per raggiungimento obiettivo',
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} badge assegnati')

    def create_events(self):
        """Crea eventi"""
        self.stdout.write('📅 Eventi...')
        
        now = timezone.now()
        organizers = User.objects.filter(is_superuser=False)
        
        events_data = [
            {
                'title': 'Workshop Python Avanzato',
                'description': 'Approfondimento su decorators, generators e async/await',
                'event_type': 'workshop',
                'start_date': now + timedelta(days=7),
                'end_date': now + timedelta(days=7),
                'location': 'Sala Riunioni A',
                'max_participants': 20,
                'is_online': False,
            },
            {
                'title': 'Tech Talk: Microservizi con Docker',
                'description': 'Introduzione all\'architettura a microservizi',
                'event_type': 'talk',
                'start_date': now + timedelta(days=14),
                'end_date': now + timedelta(days=14),
                'location': 'Microsoft Teams',
                'max_participants': 50,
                'is_online': True,
            },
            {
                'title': 'Hackathon: Innovazione Digitale',
                'description': '48 ore di coding per sviluppare prototipi innovativi',
                'event_type': 'hackathon',
                'start_date': now + timedelta(days=30),
                'end_date': now + timedelta(days=32),
                'location': 'Hub Innovazione',
                'max_participants': 40,
                'is_online': False,
            },
            {
                'title': 'Networking Coffee',
                'description': 'Incontro informale per fare networking',
                'event_type': 'networking',
                'start_date': now - timedelta(days=5),
                'end_date': now - timedelta(days=5),
                'location': 'Caffetteria Aziendale',
                'max_participants': 30,
                'is_online': False,
            },
            {
                'title': 'UI/UX Design Masterclass',
                'description': 'Best practices per design di interfacce moderne',
                'event_type': 'workshop',
                'start_date': now + timedelta(days=21),
                'end_date': now + timedelta(days=21),
                'location': 'Sala Design',
                'max_participants': 15,
                'is_online': False,
            },
        ]
        
        count = 0
        for event_data in events_data:
            organizer = random.choice(organizers)
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    **event_data,
                    'organizer': organizer,
                }
            )
            if created:
                count += 1
        
        self.stdout.write(f'  ✓ {count} eventi creati')

    def create_event_registrations(self):
        """Crea registrazioni agli eventi"""
        self.stdout.write('📝 Registrazioni Eventi...')
        
        events = Event.objects.all()
        users = User.objects.filter(is_superuser=False)
        
        count = 0
        for event in events:
            # Ogni evento ha 5-15 partecipanti
            num_participants = random.randint(5, min(15, event.max_participants))
            participants = random.sample(list(users), min(num_participants, len(users)))
            
            for user in participants:
                registration, created = EventRegistration.objects.get_or_create(
                    event=event,
                    user=user,
                    defaults={
                        'status': random.choice(['registered', 'confirmed', 'confirmed']),
                        'registered_at': timezone.now() - timedelta(days=random.randint(1, 10))
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} registrazioni create')

    def create_mentorships(self):
        """Crea relazioni di mentorship"""
        self.stdout.write('👥 Mentorship...')
        
        mentorships_data = [
            ('mario.rossi', 'luca.verdi', ['Python', 'Django', 'Best Practices']),
            ('giulia.bianchi', 'elena.conti', ['Design', 'Creatività', 'Brand']),
            ('anna.neri', 'elena.conti', ['Marketing', 'Content Strategy']),
            ('sara.ferrari', 'marco.ricci', ['Project Management', 'Agile']),
            ('francesco.russo', 'marco.ricci', ['Data Analysis', 'Python']),
            ('alessandro.bruno', 'luca.verdi', ['DevOps', 'Docker', 'CI/CD']),
            ('mario.rossi', 'chiara.moretti', ['Backend', 'API Design']),
        ]
        
        count = 0
        for mentor_username, mentee_username, focus_areas in mentorships_data:
            try:
                mentor = User.objects.get(username=mentor_username)
                mentee = User.objects.get(username=mentee_username)
                
                mentorship, created = Mentorship.objects.get_or_create(
                    mentor=mentor,
                    mentee=mentee,
                    defaults={
                        'status': random.choice(['active', 'active', 'completed']),
                        'focus_areas': focus_areas,
                        'description': f'Mentorship su {", ".join(focus_areas)}',
                        'start_date': timezone.now().date() - timedelta(days=random.randint(30, 90)),
                        'created_by': mentor,
                    }
                )
                if created:
                    count += 1
            except User.DoesNotExist:
                pass
        
        self.stdout.write(f'  ✓ {count} mentorship create')

    def create_mentorship_sessions(self):
        """Crea sessioni di mentorship"""
        self.stdout.write('📖 Sessioni Mentorship...')
        
        mentorships = Mentorship.objects.filter(status__in=['active', 'completed'])
        
        count = 0
        for mentorship in mentorships:
            # Ogni mentorship ha 2-5 sessioni
            num_sessions = random.randint(2, 5)
            
            for i in range(num_sessions):
                days_ago = random.randint(5, 60)
                session_date = timezone.now() - timedelta(days=days_ago)
                
                session, created = MentorshipSession.objects.get_or_create(
                    mentorship=mentorship,
                    session_date=session_date,
                    defaults={
                        'duration_minutes': random.choice([30, 60, 90]),
                        'location': random.choice(['Sala Riunioni', 'Online - Teams', 'Caffetteria']),
                        'agenda': 'Discussione su obiettivi e progressi',
                        'notes': 'Sessione produttiva con buoni spunti di riflessione',
                        'rating': random.randint(4, 5),
                        'completed': True,
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} sessioni create')

    def create_challenges(self):
        """Crea challenge collaborative"""
        self.stdout.write('🏆 Challenge...')
        
        now = timezone.now()
        creators = User.objects.filter(is_superuser=False)
        
        challenges_data = [
            {
                'title': 'Innovazione Inclusiva 2024',
                'description': 'Proponi un\'idea innovativa che promuova la diversità e l\'inclusione in azienda.',
                'goal': 'Sviluppare almeno 3 idee concrete con team eterogenei',
                'rules': 'Team di 4-6 persone con almeno 3 dipartimenti diversi rappresentati',
                'points': 100,
                'start_date': now.date() - timedelta(days=10),
                'end_date': now.date() + timedelta(days=20),
                'status': 'active',
            },
            {
                'title': 'Skill Sharing Week',
                'description': 'Condividi le tue competenze organizzando micro-workshop per i colleghi.',
                'goal': 'Organizzare almeno 10 micro-workshop aziendali',
                'rules': 'Workshop di 30-60 minuti su competenze specifiche',
                'points': 50,
                'start_date': now.date() + timedelta(days=7),
                'end_date': now.date() + timedelta(days=14),
                'status': 'active',
            },
            {
                'title': 'Mentorship Marathon',
                'description': 'Partecipa attivamente a programmi di mentorship come mentor o mentee.',
                'goal': 'Completare almeno 5 sessioni di mentorship',
                'rules': 'Sessioni documentate con feedback reciproco',
                'points': 75,
                'start_date': now.date() - timedelta(days=30),
                'end_date': now.date() - timedelta(days=1),
                'status': 'completed',
            },
        ]
        
        count = 0
        for challenge_data in challenges_data:
            creator = random.choice(creators)
            challenge, created = Challenge.objects.get_or_create(
                title=challenge_data['title'],
                defaults={
                    **challenge_data,
                    'created_by': creator,
                }
            )
            if created:
                count += 1
        
        self.stdout.write(f'  ✓ {count} challenge create')

    def create_challenge_participations(self):
        """Crea partecipazioni alle challenge"""
        self.stdout.write('🎯 Partecipazioni Challenge...')
        
        challenges = Challenge.objects.all()
        users = User.objects.filter(is_superuser=False)
        
        count = 0
        for challenge in challenges:
            # Ogni challenge ha 3-8 partecipanti
            num_participants = random.randint(3, 8)
            participants = random.sample(list(users), min(num_participants, len(users)))
            
            for user in participants:
                completed = challenge.status == 'completed'
                points = random.randint(0, challenge.points) if completed else 0
                
                participation, created = ChallengeParticipation.objects.get_or_create(
                    challenge=challenge,
                    user=user,
                    defaults={
                        'points_earned': points,
                        'completed': completed,
                        'completed_at': timezone.now() if completed else None,
                        'progress_data': {
                            'activities_completed': random.randint(0, 10),
                            'team_size': random.randint(3, 6),
                        }
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} partecipazioni create')

    # ========== NUOVE FUNZIONI: PROJECTS ==========

    def create_projects(self):
        """Crea progetti collaborativi"""
        self.stdout.write('🚀 Progetti...')
        
        now = timezone.now()
        managers = User.objects.filter(is_staff=True)
        
        projects_data = [
            {
                'title': 'Piattaforma E-Learning Interna',
                'description': 'Sviluppo di una piattaforma e-learning per la formazione aziendale con corsi interattivi, quiz e certificazioni.',
                'status': 'active',
                'priority': 'high',
                'team_size_min': 5,
                'team_size_max': 8,
                'start_date': now.date() - timedelta(days=15),
                'end_date': now.date() + timedelta(days=90),
                'budget': 50000.00,
                'estimated_duration_weeks': 12,
            },
            {
                'title': 'Dashboard Analytics Real-time',
                'description': 'Creazione di una dashboard per visualizzazione real-time di metriche aziendali con grafici interattivi e report automatici.',
                'status': 'active',
                'priority': 'urgent',
                'team_size_min': 4,
                'team_size_max': 6,
                'start_date': now.date() - timedelta(days=30),
                'end_date': now.date() + timedelta(days=60),
                'budget': 35000.00,
                'estimated_duration_weeks': 10,
            },
            {
                'title': 'App Mobile Talent Mosaic',
                'description': 'Sviluppo app mobile iOS/Android per gestione competenze, eventi e mentorship in mobilità.',
                'status': 'draft',
                'priority': 'medium',
                'team_size_min': 6,
                'team_size_max': 10,
                'start_date': now.date() + timedelta(days=14),
                'end_date': now.date() + timedelta(days=180),
                'budget': 80000.00,
                'estimated_duration_weeks': 20,
            },
            {
                'title': 'Sistema di Matching AI',
                'description': 'Implementazione algoritmo ML per matching automatico tra skill e progetti basato su competenze e preferenze.',
                'status': 'matching',
                'priority': 'high',
                'team_size_min': 3,
                'team_size_max': 5,
                'start_date': now.date() - timedelta(days=7),
                'end_date': now.date() + timedelta(days=75),
                'budget': 40000.00,
                'estimated_duration_weeks': 11,
            },
            {
                'title': 'Redesign UI/UX Piattaforma',
                'description': 'Completo redesign dell\'interfaccia con focus su accessibilità, usabilità e modern design patterns.',
                'status': 'open',
                'priority': 'medium',
                'team_size_min': 3,
                'team_size_max': 4,
                'start_date': now.date() + timedelta(days=30),
                'end_date': now.date() + timedelta(days=120),
                'budget': 25000.00,
                'estimated_duration_weeks': 12,
            },
            {
                'title': 'Integrazione API Esterne',
                'description': 'Integrazione con sistemi HR, calendario aziendale, e piattaforme di comunicazione (Teams, Slack).',
                'status': 'active',
                'priority': 'medium',
                'team_size_min': 2,
                'team_size_max': 4,
                'start_date': now.date() - timedelta(days=20),
                'end_date': now.date() + timedelta(days=50),
                'budget': 20000.00,
                'estimated_duration_weeks': 8,
            },
            {
                'title': 'Sistema Gamification Avanzato',
                'description': 'Implementazione sistema punti, livelli, achievements e leaderboard per aumentare engagement.',
                'status': 'completed',
                'priority': 'low',
                'team_size_min': 3,
                'team_size_max': 5,
                'start_date': now.date() - timedelta(days=90),
                'end_date': now.date() - timedelta(days=15),
                'budget': 30000.00,
                'estimated_duration_weeks': 10,
            },
        ]
        
        count = 0
        for project_data in projects_data:
            manager = random.choice(managers)
            creator = random.choice(managers)
            
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    **project_data,
                    'manager': manager,
                    'created_by': creator,
                }
            )
            if created:
                count += 1
        
        self.stdout.write(f'  ✓ {count} progetti creati')

    def create_project_skills(self):
        """Assegna skill richieste ai progetti"""
        self.stdout.write('🎯 Skill Progetti...')
        
        project_skills_mapping = {
            'Piattaforma E-Learning Interna': [
                ('Django', 5, 'required'),
                ('React', 4, 'required'),
                ('PostgreSQL', 3, 'required'),
                ('UI/UX Design', 4, 'preferred'),
                ('Docker', 3, 'nice_to_have'),
            ],
            'Dashboard Analytics Real-time': [
                ('Python for Data Science', 5, 'required'),
                ('React', 4, 'required'),
                ('Data Visualization', 5, 'required'),
                ('PostgreSQL', 3, 'preferred'),
            ],
            'App Mobile Talent Mosaic': [
                ('React', 4, 'required'),
                ('Node.js', 3, 'required'),
                ('UI/UX Design', 5, 'required'),
                ('MongoDB', 3, 'nice_to_have'),
            ],
            'Sistema di Matching AI': [
                ('Machine Learning', 5, 'required'),
                ('Python', 5, 'required'),
                ('Data Analysis', 4, 'required'),
                ('PostgreSQL', 3, 'preferred'),
            ],
            'Redesign UI/UX Piattaforma': [
                ('UI/UX Design', 5, 'required'),
                ('Figma', 4, 'required'),
                ('Graphic Design', 4, 'preferred'),
                ('JavaScript', 3, 'nice_to_have'),
            ],
            'Integrazione API Esterne': [
                ('Python', 4, 'required'),
                ('Django', 4, 'required'),
                ('FastAPI', 3, 'preferred'),
                ('Docker', 3, 'nice_to_have'),
            ],
            'Sistema Gamification Avanzato': [
                ('Django', 4, 'required'),
                ('JavaScript', 3, 'required'),
                ('PostgreSQL', 3, 'required'),
                ('React', 3, 'preferred'),
            ],
        }
        
        count = 0
        for project_title, skills_list in project_skills_mapping.items():
            try:
                project = Project.objects.get(title=project_title)
                
                for skill_name, min_prof, importance in skills_list:
                    try:
                        skill = Skill.objects.get(name=skill_name)
                        
                        proj_skill, created = ProjectRequiredSkill.objects.get_or_create(
                            project=project,
                            skill=skill,
                            defaults={
                                'min_proficiency': min_prof,
                                'importance': importance,
                                'min_years_experience': 1.0 if importance == 'required' else 0.5,
                                'weight': 100 if importance == 'required' else (50 if importance == 'preferred' else 20),
                            }
                        )
                        if created:
                            count += 1
                    except Skill.DoesNotExist:
                        pass
            except Project.DoesNotExist:
                pass
        
        self.stdout.write(f'  ✓ {count} skill-progetto create')

    def create_project_roles(self):
        """Crea ruoli per i progetti"""
        self.stdout.write('👔 Ruoli Progetti...')
        
        projects = Project.objects.all()
        
        roles_templates = [
            {'title': 'Backend Developer', 'description': 'Sviluppo API e logica server-side'},
            {'title': 'Frontend Developer', 'description': 'Sviluppo interfaccia utente'},
            {'title': 'UI/UX Designer', 'description': 'Design interfaccia e user experience'},
            {'title': 'Project Lead', 'description': 'Coordinamento team e gestione progetto'},
            {'title': 'Data Scientist', 'description': 'Analisi dati e machine learning'},
            {'title': 'DevOps Engineer', 'description': 'Infrastruttura e deployment'},
        ]
        
        count = 0
        for project in projects:
            # Ogni progetto ha 2-4 ruoli diversi
            num_roles = random.randint(2, 4)
            project_roles = random.sample(roles_templates, num_roles)
            
            for role_data in project_roles:
                role, created = ProjectRole.objects.get_or_create(
                    project=project,
                    title=role_data['title'],
                    defaults={
                        'description': role_data['description'],
                        'positions_available': random.randint(1, 3),
                        'positions_filled': 0,
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} ruoli creati')

    def create_team_members(self):
        """Assegna membri ai team dei progetti"""
        self.stdout.write('👥 Team Members...')
        
        projects = Project.objects.filter(status__in=['active', 'matching'])
        users = User.objects.filter(is_superuser=False)
        
        count = 0
        for project in projects:
            roles = ProjectRole.objects.filter(project=project)
            
            # Ogni progetto ha 3-6 membri
            num_members = random.randint(3, min(6, project.team_size_max))
            members = random.sample(list(users), min(num_members, len(users)))
            
            for i, user in enumerate(members):
                role = random.choice(roles) if roles else None
                status = random.choice(['invited', 'accepted', 'accepted', 'accepted'])
                
                member, created = TeamMember.objects.get_or_create(
                    project=project,
                    user=user,
                    defaults={
                        'role': role,
                        'status': status,
                        'match_score': random.uniform(60.0, 95.0),
                        'match_reasoning': {
                            'skill_match': random.uniform(0.7, 1.0),
                            'experience_match': random.uniform(0.6, 0.95),
                            'availability': random.choice([True, True, False]),
                        },
                        # invited_at è auto_now_add, non va settato
                        # responded_at e joined_at settabili solo se accettato
                        'responded_at': timezone.now() - timedelta(days=random.randint(1, 15)) if status in ['accepted', 'declined'] else None,
                        'joined_at': timezone.now() - timedelta(days=random.randint(1, 10)) if status == 'accepted' else None,
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} team members aggiunti')

    def create_ai_matching_runs(self):
        """Crea run di AI matching per i progetti"""
        self.stdout.write('🤖 AI Matching Runs...')
        
        projects = Project.objects.filter(status='matching')
        admins = User.objects.filter(is_staff=True)
        
        count = 0
        for project in projects:
            # Ogni progetto in matching ha 1-2 run
            num_runs = random.randint(1, 2)
            
            for i in range(num_runs):
                admin = random.choice(admins) if admins else None
                
                run, created = AIMatchingRun.objects.get_or_create(
                    project=project,
                    executed_by=admin,
                    defaults={
                        'parameters': {
                            'skill_weight': 0.4,
                            'experience_weight': 0.25,
                            'availability_weight': 0.2,
                            'diversity_bonus': 0.15,
                        },
                        'candidates_found': random.randint(5, 15),
                        'candidates_data': [
                            {
                                'user_id': random.randint(1, 10),
                                'username': f'user_{random.randint(1, 10)}',
                                'match_score': random.uniform(60.0, 98.0),
                                'skill_matches': random.randint(3, 8),
                            }
                            for _ in range(random.randint(5, 10))
                        ],
                        'execution_time_seconds': random.uniform(2.5, 25.0),
                        'success': random.choice([True, True, True, False]),
                        'error_message': 'Timeout durante l\'analisi' if random.random() > 0.8 else '',
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} AI matching runs creati')

    def create_admin_actions(self):
        """Crea log di azioni admin"""
        self.stdout.write('📋 Admin Actions...')
        
        admins = User.objects.filter(is_staff=True)
        projects = Project.objects.all()
        
        if not admins or not projects:
            self.stdout.write('  ⚠️  Nessun admin o progetto trovato')
            return
        
        actions_data = [
            ('create', 'Progetto creato'),
            ('update', 'Status progetto aggiornato'),
            ('create', 'Nuovo progetto aggiunto al sistema'),
            ('approve', 'Team member approvato'),
            ('update', 'Budget progetto modificato'),
            ('matching', 'Esecuzione algoritmo AI matching'),
            ('update', 'Scadenza progetto posticipata'),
            ('export', 'Export dati progetto in CSV'),
        ]
        
        count = 0
        for action_type, description in actions_data:
            admin = random.choice(admins)
            project = random.choice(projects)
            
            action = AdminAction.objects.create(
                admin=admin,
                action_type=action_type,
                content_type='Project',
                object_id=project.id,
                object_repr=project.title,
                description=f'{description}: {project.title}',
                changes={
                    'timestamp': str(timezone.now()),
                    'project_id': project.id,
                    'project_status': project.status,
                },
                ip_address=f'192.168.1.{random.randint(1, 255)}',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            )
            count += 1
        
        self.stdout.write(f'  ✓ {count} admin actions create')

    def create_analytics_data(self):
        """Crea dati di analytics per gli utenti"""
        self.stdout.write('📊 Analytics Data...')
        
        users = User.objects.filter(is_superuser=False)
        
        # Azioni disponibili in ActivityLog.ACTION_TYPES
        activities = [
            ('login', None, None),
            ('logout', None, None),
            ('profile_update', 'UserProfile', None),
            ('skill_add', 'Skill', None),
            ('event_register', 'Event', None),
            ('badge_earned', 'Badge', None),
        ]
        
        count = 0
        for user in users:
            # Ogni utente ha 10-30 attività
            num_activities = random.randint(10, 30)
            
            for i in range(num_activities):
                days_ago = random.randint(1, 90)
                action, entity_type, entity_id = random.choice(activities)
                
                activity, created = ActivityLog.objects.get_or_create(
                    user=user,
                    action=action,
                    created_at=timezone.now() - timedelta(days=days_ago, hours=random.randint(0, 23)),
                    defaults={
                        'entity_type': entity_type or '',
                        'entity_id': entity_id or random.randint(1, 10),
                        'ip_address': f'192.168.1.{random.randint(1, 255)}',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'metadata': {
                            'session_id': f'session_{random.randint(1000, 9999)}',
                            'duration_seconds': random.randint(60, 3600),
                        }
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} attività analytics create')

    def print_summary(self):
        """Stampa riepilogo dei dati creati"""
        self.stdout.write('\n📊 RIEPILOGO DATI:')
        self.stdout.write('\n   === DATI ESISTENTI ===')
        self.stdout.write(f'   👤 Utenti: {User.objects.filter(is_superuser=False).count()}')
        self.stdout.write(f'   📁 Categorie Competenze: {SkillCategory.objects.count()}')
        self.stdout.write(f'   🧠 Competenze: {Skill.objects.count()}')
        self.stdout.write(f'   🎯 Competenze-Utente: {UserSkill.objects.count()}')
        self.stdout.write(f'   🏅 Badge: {Badge.objects.count()}')
        self.stdout.write(f'   🎖️  Badge Assegnati: {UserBadge.objects.count()}')
        self.stdout.write(f'   📅 Eventi: {Event.objects.count()}')
        self.stdout.write(f'   📝 Registrazioni: {EventRegistration.objects.count()}')
        self.stdout.write(f'   👥 Mentorship: {Mentorship.objects.count()}')
        self.stdout.write(f'   📖 Sessioni: {MentorshipSession.objects.count()}')
        self.stdout.write(f'   🏆 Challenge: {Challenge.objects.count()}')
        self.stdout.write(f'   🎯 Partecipazioni: {ChallengeParticipation.objects.count()}')
        
        self.stdout.write('\n   === NUOVI DATI (PROJECTS & ANALYTICS) ===')
        self.stdout.write(f'   🚀 Progetti: {Project.objects.count()}')
        self.stdout.write(f'   🎯 Skill Progetti: {ProjectRequiredSkill.objects.count()}')
        self.stdout.write(f'   👔 Ruoli: {ProjectRole.objects.count()}')
        self.stdout.write(f'   👥 Team Members: {TeamMember.objects.count()}')
        self.stdout.write(f'   🤖 AI Matching Runs: {AIMatchingRun.objects.count()}')
        self.stdout.write(f'   📋 Admin Actions: {AdminAction.objects.count()}')
        self.stdout.write(f'   📊 Activity Logs: {ActivityLog.objects.count()}')
        
        self.stdout.write('\n💡 CREDENZIALI DEMO:')
        self.stdout.write('   👤 User: mario.rossi / demo123 (Staff/Admin)')
        self.stdout.write('   👤 User: anna.neri / demo123 (Staff/Admin)')
        self.stdout.write('   👤 User: giulia.bianchi / demo123')
        self.stdout.write('   👤 User: luca.verdi / demo123')
        
        self.stdout.write('\n🎯 PROGETTI CREATI:')
        projects = Project.objects.all()
        for project in projects:
            status_icon = {
                'draft': '📝',
                'open': '🔓',
                'active': '🚀',
                'matching': '🤖',
                'completed': '✅',
                'cancelled': '❌'
            }.get(project.status, '❓')
            
            self.stdout.write(f'   {status_icon} {project.title} ({project.get_status_display()})')
