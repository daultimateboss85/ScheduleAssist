# Generated by Django 4.2.6 on 2023-12-16 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0007_alter_schedule_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulecalendar',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
