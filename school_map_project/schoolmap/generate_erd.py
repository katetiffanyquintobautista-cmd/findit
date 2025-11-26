import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmap.settings')
django.setup()

from django.core.management import call_command

def generate_erd():
    output_file = 'erd.png'
    try:
        call_command('graph_models', 
                    'mapapp', 
                    '--group-models',
                    '--all-applications',
                    '--output=' + output_file)
        print(f"ERD generated successfully: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Error generating ERD: {str(e)}")

if __name__ == '__main__':
    generate_erd()
