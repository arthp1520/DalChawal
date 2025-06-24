import random
from django.core.management.base import BaseCommand
from faker import Faker
from apps.dashboard.models import User
from django.contrib.auth.hashers import make_password
from django.core.files import File
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate 15 fake users with bios and profile images'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Static images path (adjusted from your input)
        image_dir = Path('apps/dashboard/static/images/profile_images')
        image_paths = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png'))

        if not image_paths:
            self.stdout.write(self.style.WARNING("⚠️ No images found in static/images/profile_images"))
            return

        for _ in range(100):
            name = fake.user_name()
            email = fake.email()
            mobile = fake.msisdn()[:10]
            password = make_password("test1234")
            bio = fake.sentence(nb_words=12)

            selected_image_path = random.choice(image_paths)

            with open(selected_image_path, 'rb') as img:
                user = User.objects.create(
                    name=name,
                    email=email,
                    mobile=f"+91{mobile}",
                    password=password,
                    is_active=True,
                    bio=bio,
                )
                user.profile_image.save(selected_image_path.name, File(img), save=True)

        self.stdout.write(self.style.SUCCESS('✅ 15 fake users with bios and profile images created.'))
