# Generated by Django 3.2.4 on 2021-08-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GuardianArea', '0003_alter_child_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='slug',
            field=models.SlugField(default='8xbz', help_text='Do not change it', max_length=5, primary_key=True, serialize=False),
        ),
    ]
