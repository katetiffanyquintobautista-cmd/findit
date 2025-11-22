from django.db import migrations

def create_initial_data(apps, schema_editor):
    # Get models
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('mapapp', 'UserProfile')
    Building = apps.get_model('mapapp', 'Building')
    Room = apps.get_model('mapapp', 'Room')
    Subject = apps.get_model('mapapp', 'Subject')
    Section = apps.get_model('mapapp', 'Section')
    Schedule = apps.get_model('mapapp', 'Schedule')
    StudentEnrollment = apps.get_model('mapapp', 'StudentEnrollment')
    
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
    
    # Create teacher user
    teacher, created = User.objects.get_or_create(
        username='teacher',
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
        
    # Create or update teacher profile
    teacher_profile, _ = UserProfile.objects.get_or_create(
        user=teacher,
        defaults={'role': 'teacher'}
    )
    if teacher_profile.role != 'teacher':
        teacher_profile.role = 'teacher'
        teacher_profile.save()
    
    # Create schedules
    Schedule.objects.get_or_create(
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
    
    Schedule.objects.get_or_create(
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
    
    # Create student user
    student, created = User.objects.get_or_create(
        username='student',
        defaults={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'student@example.com'
        }
    )
    
    if created:
        student.set_password('student123')
        student.save()
    
    # Create or update student profile
    student_profile, _ = UserProfile.objects.get_or_create(
        user=student,
        defaults={'role': 'student'}
    )
    if student_profile.role != 'student':
        student_profile.role = 'student'
        student_profile.save()
    
    # Enroll student in section_a
    StudentEnrollment.objects.get_or_create(
        student=student,
        section=section_a,
        academic_year='2024-2025',
        defaults={'is_active': True}
    )

def delete_initial_data(apps, schema_editor):
    # This function will be used to reverse the migration if needed
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('mapapp', '0004_initial_data'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, delete_initial_data),
    ]
