# Generated by Django 3.2.4 on 2021-12-19 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GuardianArea', '0049_child_guardian'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='is_assign',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='child',
            name='is_demo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='child',
            name='is_permanent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='child',
            name='is_reserved',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='child',
            name='is_short',
            field=models.BooleanField(default=True),
        ),
    ]
