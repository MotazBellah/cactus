# Generated by Django 3.2 on 2021-04-25 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cactusApp', '0002_measurement_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='birthday',
            field=models.DateField(),
        ),
    ]
