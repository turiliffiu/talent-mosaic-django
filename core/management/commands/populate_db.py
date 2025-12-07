"""
Management command per popolare il database con dati di esempio realistici
Uso: python manage.py populate_db [--flush]
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


class Command(BaseCommand):
    help = 'Popola il database con dati di esempio per demo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Elimina tutti i dati esistenti prima di popolare',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎯 TALENT MOSAIC - Popolamento Database Demo'))
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
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('✅ Popolamento completato con successo!'))
        self.print_summary()

    def flush_data(self):
        """Elimina tutti i dati (esclusi superuser)"""
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
                'profile': {
                    'job_title': 'Senior Software Engineer',
                    'department': 'IT Development',
                    'bio': 'Appassionato di tecnologia con 10 anni di esperienza nello sviluppo software. Mi piace condividere conoscenze e fare mentoring.',
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
                    'bio': 'Designer creativa con passione per la user experience. Cerco sempre di creare interfacce intuitive e belle.',
                    'location': 'Roma, Italia',
                    'is_mentor': True,
                    'is_mentee': True,
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
                    'bio': 'Giovane sviluppatore in crescita. Entusiasta di imparare nuove tecnologie e best practices.',
                    'location': 'Torino, Italia',
                    'is_mentor': False,
                    'is_mentee': True,
                }
            },
            {
                'username': 'anna.neri',
                'first_name': 'Anna',
                'last_name': 'Neri',
                'email': 'anna.neri@fibercop.it',
                'profile': {
                    'job_title': 'Marketing Manager',
                    'department': 'Marketing',
                    'bio': 'Esperta di marketing digitale e strategie di comunicazione. Sempre alla ricerca di nuove opportunità di crescita.',
                    'location': 'Milano, Italia',
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
                    'department': 'Data Analytics',
                    'bio': 'Data scientist con background in statistica e machine learning. Mi piace trovare insight dai dati.',
                    'location': 'Bologna, Italia',
                    'is_mentor': True,
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
                    'department': 'PMO',
                    'bio': 'Project manager certificata PMP. Esperta nella gestione di progetti complessi e team distribuiti.',
                    'location': 'Firenze, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
            {
                'username': 'davide.esposito',
                'first_name': 'Davide',
                'last_name': 'Esposito',
                'email': 'davide.esposito@fibercop.it',
                'profile': {
                    'job_title': 'DevOps Engineer',
                    'department': 'IT Operations',
                    'bio': 'Esperto in cloud infrastructure e automazione. Appassionato di container e CI/CD.',
                    'location': 'Napoli, Italia',
                    'is_mentor': True,
                    'is_mentee': True,
                }
            },
            {
                'username': 'elena.conti',
                'first_name': 'Elena',
                'last_name': 'Conti',
                'email': 'elena.conti@fibercop.it',
                'profile': {
                    'job_title': 'Content Specialist',
                    'department': 'Marketing',
                    'bio': 'Creatrice di contenuti digitali con focus su storytelling e brand communication.',
                    'location': 'Palermo, Italia',
                    'is_mentor': False,
                    'is_mentee': True,
                }
            },
            {
                'username': 'marco.ricci',
                'first_name': 'Marco',
                'last_name': 'Ricci',
                'email': 'marco.ricci@fibercop.it',
                'profile': {
                    'job_title': 'Business Analyst',
                    'department': 'Strategy',
                    'bio': 'Business analyst con esperienza in digital transformation e process optimization.',
                    'location': 'Genova, Italia',
                    'is_mentor': True,
                    'is_mentee': True,
                }
            },
            {
                'username': 'chiara.lombardi',
                'first_name': 'Chiara',
                'last_name': 'Lombardi',
                'email': 'chiara.lombardi@fibercop.it',
                'profile': {
                    'job_title': 'HR Specialist',
                    'department': 'Human Resources',
                    'bio': 'Specialista HR con focus su talent development e diversity & inclusion.',
                    'location': 'Milano, Italia',
                    'is_mentor': True,
                    'is_mentee': False,
                }
            },
        ]
        
        count = 0
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                }
            )
            
            if created:
                user.set_password('demo123')  # Password uguale per tutti in demo
                user.save()
                
                # Aggiorna profilo
                profile = user.profile
                for key, value in user_data['profile'].items():
                    setattr(profile, key, value)
                profile.save()
                
                count += 1
        
        self.stdout.write(f'  ✓ {count} utenti creati (password: demo123)')

    def create_user_skills(self):
        """Associa competenze agli utenti"""
        self.stdout.write('🎯 Associazione Competenze Utenti...')
        
        # Mappatura utenti -> competenze (realistico basato sul ruolo)
        user_skills_map = {
            'mario.rossi': ['Python', 'Django', 'JavaScript', 'React', 'PostgreSQL', 'Docker', 'Git'],
            'giulia.bianchi': ['UI/UX Design', 'Figma', 'Adobe Photoshop', 'Graphic Design', 'Branding'],
            'luca.verdi': ['Python', 'JavaScript', 'Git', 'SQL'],
            'anna.neri': ['Content Marketing', 'SEO', 'Social Media Marketing', 'Copywriting'],
            'francesco.russo': ['Python for Data Science', 'Machine Learning', 'Statistics', 'SQL for Analytics', 'Tableau'],
            'sara.ferrari': ['Project Management', 'Agile', 'Scrum', 'Stakeholder Management', 'Team Leadership'],
            'davide.esposito': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Python', 'Git'],
            'elena.conti': ['Copywriting', 'Content Marketing', 'Social Media Marketing', 'Public Speaking'],
            'marco.ricci': ['Data Analysis', 'Excel', 'SQL', 'Strategic Planning', 'Problem Solving'],
            'chiara.lombardi': ['People Management', 'Coaching', 'Public Speaking', 'Conflict Resolution', 'Empatia'],
        }
        
        count = 0
        for username, skills_list in user_skills_map.items():
            try:
                user = User.objects.get(username=username)
                for skill_name in skills_list:
                    try:
                        skill = Skill.objects.get(name=skill_name)
                        # Proficiency random tra 2 e 5 (più realistico)
                        proficiency = random.randint(2, 5)
                        years = round(random.uniform(0.5, 10.0), 1)
                        
                        user_skill, created = UserSkill.objects.get_or_create(
                            user=user,
                            skill=skill,
                            defaults={
                                'proficiency': proficiency,
                                'years_experience': years,
                                'verified': random.choice([True, False]),
                            }
                        )
                        if created:
                            count += 1
                    except Skill.DoesNotExist:
                        pass
            except User.DoesNotExist:
                pass
        
        self.stdout.write(f'  ✓ {count} associazioni create')

    def create_badges(self):
        """Crea badge del sistema"""
        self.stdout.write('🏅 Badge...')
        
        badges_data = [
            {
                'name': 'Primo Passo',
                'description': 'Completa il tuo profilo per la prima volta',
                'rarity': 'common',
                'points': 10,
                'color': '#10B981',
            },
            {
                'name': 'Esperto di Competenze',
                'description': 'Aggiungi almeno 5 competenze al tuo profilo',
                'rarity': 'uncommon',
                'points': 25,
                'color': '#3B82F6',
            },
            {
                'name': 'Mentor Dedicato',
                'description': 'Completa 3 sessioni di mentorship',
                'rarity': 'rare',
                'points': 50,
                'color': '#F59E0B',
            },
            {
                'name': 'Team Player',
                'description': 'Partecipa a 5 eventi aziendali',
                'rarity': 'uncommon',
                'points': 30,
                'color': '#06B6D4',
            },
            {
                'name': 'Innovatore',
                'description': 'Completa una challenge sulla diversità',
                'rarity': 'rare',
                'points': 75,
                'color': '#8B5CF6',
            },
            {
                'name': 'Campione della Diversità',
                'description': 'Partecipa attivamente a iniziative D&I',
                'rarity': 'epic',
                'points': 100,
                'color': '#EC4899',
            },
            {
                'name': 'Leggenda Talent Mosaic',
                'description': 'Raggiungi il massimo livello di engagement',
                'rarity': 'legendary',
                'points': 200,
                'color': '#EF4444',
            },
        ]
        
        count = 0
        for badge_data in badges_data:
            # Per la demo, non usiamo l'icon (ImageField)
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults={
                    'description': badge_data['description'],
                    'rarity': badge_data['rarity'],
                    'points': badge_data['points'],
                    'color': badge_data['color'],
                    'is_active': True,
                }
            )
            if created:
                count += 1
        
        self.stdout.write(f'  ✓ {count} badge creati')

    def create_user_badges(self):
        """Assegna badge ad alcuni utenti"""
        self.stdout.write('🎖️  Assegnazione Badge...')
        
        users = User.objects.filter(is_superuser=False)
        badges = Badge.objects.all()
        
        count = 0
        for user in users:
            # Ogni utente riceve 1-3 badge random
            num_badges = random.randint(1, 3)
            selected_badges = random.sample(list(badges), min(num_badges, len(badges)))
            
            for badge in selected_badges:
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=badge,
                    defaults={
                        'notes': f'Assegnato automaticamente per demo',
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} badge assegnati')

    def create_events(self):
        """Crea eventi aziendali"""
        self.stdout.write('📅 Eventi...')
        
        now = timezone.now()
        organizers = User.objects.filter(profile__is_mentor=True)
        
        events_data = [
            {
                'title': 'Workshop Django Avanzato',
                'description': 'Impara tecniche avanzate di Django per costruire applicazioni scalabili e performanti.',
                'event_type': 'workshop',
                'start_date': now + timedelta(days=7),
                'end_date': now + timedelta(days=7, hours=3),
                'location': 'Sala Conferenze A - Milano',
                'max_participants': 20,
                'status': 'published',
            },
            {
                'title': 'Diversity & Inclusion: Best Practices',
                'description': 'Sessione interattiva sulle migliori pratiche per promuovere la diversità in azienda.',
                'event_type': 'training',
                'start_date': now + timedelta(days=14),
                'end_date': now + timedelta(days=14, hours=2),
                'location': 'Auditorium Centrale',
                'is_online': False,
                'max_participants': 50,
                'status': 'published',
            },
            {
                'title': 'Webinar: Future of Work',
                'description': 'Esplora le tendenze del futuro del lavoro con esperti del settore.',
                'event_type': 'webinar',
                'start_date': now + timedelta(days=21),
                'end_date': now + timedelta(days=21, hours=1.5),
                'is_online': True,
                'location_url': 'https://zoom.us/j/example',
                'max_participants': 100,
                'status': 'published',
            },
            {
                'title': 'Team Building: Escape Room Virtuale',
                'description': 'Attività di team building per rafforzare la collaborazione tra colleghi.',
                'event_type': 'social',
                'start_date': now + timedelta(days=10),
                'end_date': now + timedelta(days=10, hours=2),
                'is_online': True,
                'max_participants': 30,
                'status': 'published',
            },
            {
                'title': 'Conferenza Annuale Innovazione',
                'description': 'La nostra conferenza annuale dedicata all\'innovazione tecnologica e organizzativa.',
                'event_type': 'conference',
                'start_date': now + timedelta(days=30),
                'end_date': now + timedelta(days=30, hours=8),
                'location': 'Centro Congressi Milano',
                'max_participants': 200,
                'status': 'published',
            },
            {
                'title': 'Workshop UX/UI Design Thinking',
                'description': 'Impara i principi del design thinking applicato alla user experience.',
                'event_type': 'workshop',
                'start_date': now - timedelta(days=5),  # Evento passato
                'end_date': now - timedelta(days=5, hours=-3),
                'location': 'Sala Design - Roma',
                'max_participants': 15,
                'status': 'completed',
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
            num_participants = random.randint(5, min(15, event.max_participants or 15))
            participants = random.sample(list(users), min(num_participants, len(users)))
            
            for user in participants:
                # Eventi passati hanno status 'attended' o 'no_show'
                if event.status == 'completed':
                    status = random.choice(['attended', 'attended', 'attended', 'no_show'])
                    rating = random.randint(3, 5) if status == 'attended' else None
                else:
                    status = 'registered'
                    rating = None
                
                registration, created = EventRegistration.objects.get_or_create(
                    event=event,
                    user=user,
                    defaults={
                        'status': status,
                        'rating': rating,
                        'feedback': 'Evento molto interessante!' if rating else '',
                    }
                )
                if created:
                    count += 1
        
        self.stdout.write(f'  ✓ {count} registrazioni create')

    def create_mentorships(self):
        """Crea relazioni di mentorship"""
        self.stdout.write('👥 Mentorship...')
        
        mentors = User.objects.filter(profile__is_mentor=True)
        mentees = User.objects.filter(profile__is_mentee=True)
        
        mentorships_data = [
            ('mario.rossi', 'luca.verdi', ['Python', 'Django', 'Best Practices']),
            ('giulia.bianchi', 'elena.conti', ['Design', 'Creatività', 'Brand']),
            ('anna.neri', 'elena.conti', ['Marketing', 'Content Strategy']),
            ('sara.ferrari', 'marco.ricci', ['Project Management', 'Agile']),
            ('francesco.russo', 'marco.ricci', ['Data Analysis', 'Python']),
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

    def print_summary(self):
        """Stampa riepilogo dei dati creati"""
        self.stdout.write('\n📊 RIEPILOGO DATI:')
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
        
        self.stdout.write('\n💡 CREDENZIALI DEMO:')
        self.stdout.write('   Username: [qualsiasi utente sopra]')
        self.stdout.write('   Password: demo123')
        self.stdout.write('\n   Es: mario.rossi / demo123')
