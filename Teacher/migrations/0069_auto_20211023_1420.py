# Generated by Django 3.2.4 on 2021-10-23 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0068_auto_20211023_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='PermanentLocationDistrict',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='PermanentLocationDistrict', to='Teacher.district'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='PermanentLocationDivision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='PermanentLocationDivision', to='Teacher.division'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='PermanentLocationThana',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='PermanentLocationThana', to='Teacher.thana'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='PresentLocationDistrict',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='PresentLocationDistrict', to='Teacher.district'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='PresentLocationDivision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='PresentLocationDivision', to='Teacher.division'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='PresentLocationThana',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='PresentLocationThana', to='Teacher.thana'),
        ),
    ]
