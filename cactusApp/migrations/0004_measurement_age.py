# Generated by Django 3.2 on 2021-04-25 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cactusApp', '0003_alter_child_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='age',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
