# Generated by Django 4.2.6 on 2023-11-30 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0002_alter_dailyevent_end_time_alter_dailyevent_schedule_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='name',
            field=models.CharField(blank=True, choices=[('0', 'Master'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursay'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], max_length=255),
        ),
    ]
