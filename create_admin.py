import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IBC_SARL.settings')
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@ibcsarl.com'
password = 'admin'

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created with password '{password}'.")
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print(f"Superuser '{username}' already exists. Password reset to '{password}'.")
except Exception as e:
    print(f"Error: {e}")
