import os
import sys
import subprocess

# Check if Django is installed
try:
    import django
    print(f"Django version: {django.get_version()}")
except ImportError:
    print("Django is not installed. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "django", "django-crispy-forms", "crispy-bootstrap5", "cryptography"])
    print("Packages installed successfully!")

# Print instructions to run the server
print("\nTo run the server, execute the following commands:")
print("1. Navigate to the project directory:")
print("   cd encrypted_email")
print("\n2. Apply migrations:")
print("   python manage.py makemigrations email_app")
print("   python manage.py migrate")
print("\n3. Create a superuser (admin):")
print("   python manage.py createsuperuser")
print("\n4. Run the development server:")
print("   python manage.py runserver")
print("\nThen open your browser and go to: http://127.0.0.1:8000/")
