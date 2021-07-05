# Generated by Django 3.2.5 on 2021-07-04 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_auto_20210704_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_pictures', to=settings.AUTH_USER_MODEL),
        ),
    ]
