# Generated by Django 3.2.4 on 2021-12-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GuardianArea', '0047_auto_20211207_2049'),
        ('FollowUp', '0025_alter_user_guardian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Guardian',
            field=models.ManyToManyField(blank=True, to='GuardianArea.GuardianDetails'),
        ),
    ]
