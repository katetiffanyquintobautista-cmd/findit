from django.db import migrations

def create_initial_data(apps, schema_editor):
    # Get models
    User = apps.get_model('auth', 'User')
    Building = apps.get_model('mapapp', 'Building')
    Room = apps.get_model('mapapp', 'Room')
    Subject = apps.get_model('mapapp', 'Subject')
    Section = apps.get_model('mapapp', 'Section')
    Schedule = apps.get_model('mapapp', 'Schedule')
    StudentEnrollment = apps.get_model('mapapp', 'StudentEnrollment')
    
    # Create buildings
    main_building = Building.objects.create(
        name='Main Building',
        code='MB',
        latitude=14.5995,
        longitude=120.9842,
        description='Main academic building with classrooms and offices.'
    )
    
    science_building = Building.objects.create(
        name='Science Building',
        code='SB',
        latitude=14.5985,
        longitude=120.9852,
        description='Building for science laboratories and classrooms.'
    )
    
    # Create rooms
    room101 = Room.objects.create(
        building=main_building,
        room_number='101',
        floor=1,
        capacity=40,
        room_type='classroom'
    )
    
    room201 = Room.objects.create(
        building=main_building,
        room_number='201',
        floor=2,
        capacity=35,
        room_type='classroom'
    )
    
    lab101 = Room.objects.create(
        building=science_building,
        room_number='101',
        floor=1,
        capacity=25,
        room_type='lab',
        description='Computer Laboratory'
    )
    
    # Create subjects
    math = Subject.objects.create(
        code='MATH101',
        name='Mathematics',
        units=3.0,
        description='Basic Mathematics course'
    )
    
    science = Subject.objects.create(
        code='SCI101',
        name='General Science',
        units=3.0,
        description='Introduction to Science'
    )
    
    # Create sections
    section_a = Section.objects.create(
        name='10-Newton',
        grade_level=10,
        academic_year='2024-2025'
    )
    
    section_b = Section.objects.create(
        name='11-Einstein',
        grade_level=11,
        academic_year='2024-2025'
    )
    
    # Get or create a teacher user
    teacher = User.objects.filter(username='teacher').first()
    if not teacher:
        teacher = User.objects.create_user(
            username='teacher',
            password='teacher123',
            first_name='John',
            last_name='Smith',
            email='teacher@example.com'
        )
        # Create profile if it doesn't exist
        from mapapp.models import UserProfile
        UserProfile.objects.get_or_create(user=teacher)
        teacher.refresh_from_db()
        teacher.profile.role = 'teacher'
        teacher.profile.save()
    
    # Create schedules
    Schedule.objects.create(
        subject=math,
        teacher=teacher,
        section=section_a,
        room=room101,
        day='monday',
        time_slot='07:30-08:30',
        academic_year='2024-2025'
    )
    
    Schedule.objects.create(
        subject=science,
        teacher=teacher,
        section=section_b,
        room=lab101,
        day='tuesday',
        time_slot='10:30-11:30',
        academic_year='2024-2025'
    )
    
    # Create a test student and enroll in section_a
    student = User.objects.filter(username='student').first()
    if not student:
        student = User.objects.create_user(
            username='student',
            password='student123',
            first_name='Jane',
            last_name='Doe',
            email='student@example.com'
        )
        # Create profile if it doesn't exist
        from mapapp.models import UserProfile
        UserProfile.objects.get_or_create(user=student)
        student.refresh_from_db()
        student.profile.role = 'student'
        student.profile.save()
    
    # Enroll student in section_a
    StudentEnrollment.objects.get_or_create(
        student=student,
        section=section_a,
        academic_year='2024-2025'
    )

def delete_initial_data(apps, schema_editor):
    # This function will be used to reverse the migration if needed
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('mapapp', '0003_building_room_section_subject_studentenrollment_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, delete_initial_data),
    ]
