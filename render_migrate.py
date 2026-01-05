import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_management.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

# 1️⃣ Run migrations
call_command("migrate", interactive=False)

# 2️⃣ Create superuser ONLY if not exists
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123"
    )
