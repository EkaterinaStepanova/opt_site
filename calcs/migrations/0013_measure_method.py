# Generated by Django 2.0.5 on 2018-05-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcs', '0012_remove_measure_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='method',
            field=models.CharField(choices=[('gs', 'global_search'), ('pi', 'piyavsky')], default='gs', max_length=2),
        ),
    ]