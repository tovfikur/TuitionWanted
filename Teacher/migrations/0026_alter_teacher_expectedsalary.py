# Generated by Django 3.2.4 on 2021-09-02 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0025_auto_20210902_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='ExpectedSalary',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Private'), (2, 'Group'), (3, 'Both')], default=2500, null=True),
        ),
    ]
