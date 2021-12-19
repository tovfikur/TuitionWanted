# Generated by Django 3.2.4 on 2021-09-02 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0027_rename_maximum_education_level_teacher_preferred_education'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='Preferred_Education',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='Preferred_Medium',
        ),
        migrations.CreateModel(
            name='TeachingSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Preferred_Education', models.SmallIntegerField(default=20, verbose_name=((0, 'Class 0'), (2, 'Class 2'), (3, 'Class 3'), (4, 'Class 4'), (5, 'Class 5'), (6, 'Class 6'), (7, 'Class 7'), (8, 'Class 8'), (9, 'Class 9'), (10, 'Class 10'), (11, 'Class 11'), (12, 'Class 12'), (20, 'Others')))),
                ('Preferred_Medium', models.SmallIntegerField(choices=[(1, 'Bangla Medium'), (2, 'English Medium'), (3, 'English Version'), (4, 'Arbi Medium'), (5, 'Arbi Version'), (6, 'Technical')], default=1)),
                ('Other', models.CharField(blank=True, max_length=200, null=True)),
                ('Preferred_Subject', models.ManyToManyField(blank=True, to='Teacher.Subject')),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='Preferred',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Preferred', to='Teacher.teachingsection'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='Experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Experience', to='Teacher.teachingsection'),
        ),
    ]
