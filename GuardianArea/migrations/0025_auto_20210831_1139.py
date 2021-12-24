# Generated by Django 3.2.4 on 2021-08-31 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0016_alter_division_name'),
        ('GuardianArea', '0024_auto_20210829_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='Expected_Subjects',
            field=models.ManyToManyField(blank=True, to='Teacher.Subject'),
        ),
        migrations.AlterField(
            model_name='child',
            name='Note',
            field=models.ManyToManyField(blank=True, to='GuardianArea.Note'),
        ),
        migrations.AlterField(
            model_name='child',
            name='Teacher_Background',
            field=models.SmallIntegerField(choices=[(1, 'General'), (2, 'Science'), (3, 'Engineer'), (4, 'Medical'), (5, 'Arts'), (6, 'Commerce'), (7, 'Technical'), (8, 'English Medium'), (9, 'English Version'), (10, 'Other')], default=3),
        ),
        migrations.AlterField(
            model_name='child',
            name='Teacher_Level',
            field=models.SmallIntegerField(choices=[(0, 'Secondary'), (1, 'Higher Secondary'), (3, 'Honors'), (4, 'Others')], default=3),
        ),
        migrations.AlterField(
            model_name='child',
            name='slug',
            field=models.SlugField(default=0, help_text='Do not change it', max_length=5, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='guardiandetails',
            name='Note',
            field=models.ManyToManyField(blank=True, to='GuardianArea.Note'),
        ),
    ]
