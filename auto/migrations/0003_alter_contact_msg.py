# Generated by Django 3.2.8 on 2022-05-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='msg',
            field=models.TextField(max_length=150),
        ),
    ]
