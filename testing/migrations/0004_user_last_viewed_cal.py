# Generated by Django 4.2.6 on 2023-12-04 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_alter_schedule_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_viewed_cal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='testing.schedulecalendar'),
        ),
    ]
