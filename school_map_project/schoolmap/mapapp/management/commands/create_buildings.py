from django.core.management.base import BaseCommand
from mapapp.models import BuildingInfo

class Command(BaseCommand):
    help = 'Create sample building data'

    def handle(self, *args, **options):
        buildings = [
            {'name': 'Library', 'description': 'Main library with study areas and computer lab'},
            {'name': 'Admin Office', 'description': 'Administrative offices and student services'},
            {'name': 'Caregiving', 'description': 'Caregiving department and training facilities'},
            {'name': 'Junior High', 'description': 'Junior high school classrooms and facilities'},
            {'name': 'Canteen 1', 'description': 'Main cafeteria serving meals and snacks'},
            {'name': 'Clinic', 'description': 'School health clinic and medical services'},
            {'name': 'Food Processing 1', 'description': 'Food processing laboratory and training center'},
            {'name': 'Food Processing 2', 'description': 'Secondary food processing facility'},
            {'name': 'Canteen 2', 'description': 'Additional dining area and food services'},
        ]
        
        for building_data in buildings:
            building, created = BuildingInfo.objects.get_or_create(
                name=building_data['name'],
                defaults={'description': building_data['description']}
            )
            if created:
                self.stdout.write(f'Created building: {building.name}')
            else:
                self.stdout.write(f'Building already exists: {building.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully created building data'))