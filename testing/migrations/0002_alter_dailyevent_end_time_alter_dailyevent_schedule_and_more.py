# Generated by Django 4.2.6 on 2023-11-30 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyevent',
            name='end_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='dailyevent',
            name='schedule',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='testing.schedule'),
        ),
        migrations.AlterField(
            model_name='dailyevent',
            name='start_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='dailyevent',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='miscellanouscalendar',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='miscellanouscalendar',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='misc_cal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='schedulecalendar',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='schedulecalendar',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_cals', to=settings.AUTH_USER_MODEL),
        ),
    ]