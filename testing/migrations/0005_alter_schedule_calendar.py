# Generated by Django 4.2.6 on 2023-12-04 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0004_user_last_viewed_cal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='calendar',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='testing.schedulecalendar'),
        ),
    ]
