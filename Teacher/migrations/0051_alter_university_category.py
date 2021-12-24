# Generated by Django 3.2.4 on 2021-10-04 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0050_teacher_handwriting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='Category',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'PUBLIC'), (2, 'NATIONAL'), (3, 'PRIVATE'), (4, 'OTHERS')], null=True),
        ),
    ]
