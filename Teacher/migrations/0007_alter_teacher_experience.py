# Generated by Django 3.2.4 on 2021-08-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0006_auto_20210822_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='Experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
