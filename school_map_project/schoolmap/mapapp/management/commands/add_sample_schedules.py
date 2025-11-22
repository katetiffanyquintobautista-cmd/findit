from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mapapp.models import Building, Room, Subject, Section, Schedule, StudentEnrollment

class Command(BaseCommand):
    help = 'Adds sample schedules to the database'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get existing objects
        main_building = Building.objects.get(name='Main Building')
        room101 = Room.objects.get(building=main_building, room_number='101')
        room201 = Room.objects.get(building=main_building, room_number='201')
        
        science_building = Building.objects.get(name='Science Building')
        lab101 = Room.objects.get(building=science_building, room_number='101')
        
        math = Subject.objects.get(code='MATH101')
        science = Subject.objects.get(code='SCI101')
        
        section_a = Section.objects.get(name='10-Newton')
        section_b = Section.objects.get(name='11-Einstein')
        
        teacher = User.objects.get(username='teacher')
        
        # Create sample schedules
        schedules = [
            # Monday
            {
                'subject': math,
                'teacher': teacher,
                'section': section_a,
                'room': room101,
                'day': 'monday',
                'time_slot': '07:30-08:30',
                'academic_year': '2024-2025',
                'is_active': True
            },
            {
                'subject': science,
                'teacher': teacher,
                'section': section_a,
                'room': lab101,
                'day': 'monday',
                'time_slot': '08:30-09:30',
                'academic_year': '2024-2025',
                'is_active': True
            },
            # Tuesday
            {
                'subject': math,
                'teacher': teacher,
                'section': section_b,
                'room': room201,
                'day': 'tuesday',
                'time_slot': '09:30-10:30',
                'academic_year': '2024-2025',
                'is_active': True
            },
            # Wednesday
            {
                'subject': science,
                'teacher': teacher,
                'section': section_b,
                'room': lab101,
                'day': 'wednesday',
                'time_slot': '10:30-11:30',
                'academic_year': '2024-2025',
                'is_active': True
            },
        ]
        
        # Create schedules
        for schedule_data in schedules:
            Schedule.objects.get_or_create(
                subject=schedule_data['subject'],
                teacher=schedule_data['teacher'],
                section=schedule_data['section'],
                day=schedule_data['day'],
                time_slot=schedule_data['time_slot'],
                defaults={
                    'room': schedule_data['room'],
                    'academic_year': schedule_data['academic_year'],
                    'is_active': schedule_data['is_active']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully added sample schedules'))
