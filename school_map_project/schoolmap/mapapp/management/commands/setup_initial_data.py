from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mapapp.models import UserProfile, Building, Room, Subject, Section, Schedule, StudentEnrollment

class Command(BaseCommand):
    help = 'Sets up initial data for the application'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create buildings
        main_building, _ = Building.objects.get_or_create(
            name='Main Building',
            code='MB',
            defaults={
                'latitude': 14.5995,
                'longitude': 120.9842,
                'description': 'Main academic building with classrooms and offices.'
            }
        )
        
        science_building, _ = Building.objects.get_or_create(
            name='Science Building',
            code='SB',
            defaults={
                'latitude': 14.5985,
                'longitude': 120.9852,
                'description': 'Building for science laboratories and classrooms.'
            }
        )
        
        # Create rooms
        room101, _ = Room.objects.get_or_create(
            building=main_building,
            room_number='101',
            defaults={
                'floor': 1,
                'capacity': 40,
                'room_type': 'classroom'
            }
        )
        
        room201, _ = Room.objects.get_or_create(
            building=main_building,
            room_number='201',
            defaults={
                'floor': 2,
                'capacity': 35,
                'room_type': 'classroom'
            }
        )
        
        lab101, _ = Room.objects.get_or_create(
            building=science_building,
            room_number='101',
            defaults={
                'floor': 1,
                'capacity': 25,
                'room_type': 'lab',
                'description': 'Computer Laboratory'
            }
        )
        
        # Create subjects
        math, _ = Subject.objects.get_or_create(
            code='MATH101',
            defaults={
                'name': 'Mathematics',
                'units': 3.0,
                'description': 'Basic Mathematics course'
            }
        )
        
        science, _ = Subject.objects.get_or_create(
            code='SCI101',
            defaults={
                'name': 'General Science',
                'units': 3.0,
                'description': 'Introduction to Science'
            }
        )
        
        # Create sections
        section_a, _ = Section.objects.get_or_create(
            name='10-Newton',
            defaults={
                'grade_level': 10,
                'academic_year': '2024-2025'
            }
        )
        
        section_b, _ = Section.objects.get_or_create(
            name='11-Einstein',
            defaults={
                'grade_level': 11,
                'academic_year': '2024-2025'
            }
        )
        
        # Create or update teacher user
        teacher_username = 'teacher'
        teacher, created = User.objects.get_or_create(
            username=teacher_username,
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'teacher@example.com',
                'is_staff': True
            }
        )
        
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(self.style.SUCCESS('Created teacher user'))
        else:
            self.stdout.write(self.style.SUCCESS('Teacher user already exists'))
        
        # Create or update teacher profile
        teacher_profile, profile_created = UserProfile.objects.get_or_create(
            user=teacher,
            defaults={'role': 'teacher'}
        )
        
        if teacher_profile.role != 'teacher':
            teacher_profile.role = 'teacher'
            teacher_profile.save()
            self.stdout.write(self.style.SUCCESS('Updated teacher profile'))
        elif profile_created:
            self.stdout.write(self.style.SUCCESS('Created teacher profile'))
        else:
            self.stdout.write(self.style.SUCCESS('Teacher profile already exists'))
        
        # Create schedules
        schedule1, created = Schedule.objects.get_or_create(
            subject=math,
            teacher=teacher,
            section=section_a,
            day='monday',
            time_slot='07:30-08:30',
            defaults={
                'room': room101,
                'academic_year': '2024-2025',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Math schedule'))
        
        schedule2, created = Schedule.objects.get_or_create(
            subject=science,
            teacher=teacher,
            section=section_b,
            day='tuesday',
            time_slot='10:30-11:30',
            defaults={
                'room': lab101,
                'academic_year': '2024-2025',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Science schedule'))
        
        # Create or update student user
        student_username = 'student'
        student, created = User.objects.get_or_create(
            username=student_username,
            defaults={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'student@example.com'
            }
        )
        
        if created:
            student.set_password('student123')
            student.save()
            self.stdout.write(self.style.SUCCESS('Created student user'))
        else:
            self.stdout.write(self.style.SUCCESS('Student user already exists'))
        
        # Create or update student profile
        student_profile, profile_created = UserProfile.objects.get_or_create(
            user=student,
            defaults={'role': 'student'}
        )
        
        if student_profile.role != 'student':
            student_profile.role = 'student'
            student_profile.save()
            self.stdout.write(self.style.SUCCESS('Updated student profile'))
        elif profile_created:
            self.stdout.write(self.style.SUCCESS('Created student profile'))
        else:
            self.stdout.write(self.style.SUCCESS('Student profile already exists'))
        
        # Enroll student in section_a if not already enrolled
        enrollment, enrollment_created = StudentEnrollment.objects.get_or_create(
            student=student,
            section=section_a,
            academic_year='2024-2025',
            defaults={'is_active': True}
        )
        
        if enrollment_created:
            self.stdout.write(self.style.SUCCESS('Enrolled student in section'))
        else:
            self.stdout.write(self.style.SUCCESS('Student already enrolled in section'))
        
        self.stdout.write(self.style.SUCCESS('Successfully set up initial data'))
