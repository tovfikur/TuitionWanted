# Generated by Django 3.2.4 on 2021-09-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FollowUp', '0013_auto_20210914_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedteacherforchild',
            name='Talks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shortlistedtuitionforchild',
            name='Talks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='temporarytuitionforchild',
            name='Talks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
