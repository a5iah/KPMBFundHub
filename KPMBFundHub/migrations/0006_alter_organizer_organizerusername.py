# Generated by Django 5.0.7 on 2024-10-13 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KPMBFundHub', '0005_remove_organizer_organizationname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='organizerUsername',
            field=models.TextField(max_length=50),
        ),
    ]
