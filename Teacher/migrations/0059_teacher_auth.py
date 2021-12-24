# Generated by Django 3.2.4 on 2021-10-13 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Teacher', '0058_alter_subject_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='auth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
