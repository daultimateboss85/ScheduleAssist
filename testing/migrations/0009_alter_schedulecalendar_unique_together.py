# Generated by Django 4.2.6 on 2023-12-16 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0008_alter_schedulecalendar_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedulecalendar',
            unique_together={('owner', 'name')},
        ),
    ]
