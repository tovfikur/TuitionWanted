# Generated by Django 3.2.4 on 2021-10-02 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GuardianArea', '0037_rename_confirmed_child_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardiandetails',
            name='Connect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='child',
            name='Education_Medium',
            field=models.SmallIntegerField(choices=[(1, 'Bangla Medium'), (2, 'English Medium'), (3, 'English Version'), (4, 'Madrasa Medium'), (7, 'Education of Quran'), (7, 'Others')], default=1),
        ),
        migrations.AlterField(
            model_name='child',
            name='Teacher_Background',
            field=models.SmallIntegerField(choices=[(1, 'General'), (2, 'Science'), (3, 'Engineer'), (4, 'Medical'), (5, 'Arts'), (6, 'Commerce'), (7, 'Technical'), (8, 'English Medium'), (9, 'English Version'), (10, 'Education of Quran'), (11, 'Other'), (100, 'All')], default=100),
        ),
        migrations.AlterField(
            model_name='child',
            name='Teacher_Medium',
            field=models.SmallIntegerField(choices=[(1, 'Bangla Medium'), (2, 'English Medium'), (3, 'English Version'), (4, 'Madrasa Medium'), (7, 'Education of Quran'), (7, 'Others')], default=1),
        ),
    ]
