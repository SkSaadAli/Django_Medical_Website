# Generated by Django 3.2.9 on 2023-08-24 15:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_auto_20230820_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_date', models.DateField(default=datetime.date.today)),
                ('chosen_time', models.TimeField(default=datetime.time(12, 0))),
                ('end_time', models.TimeField(default=datetime.time(12, 45))),
                ('google_url', models.URLField(max_length=300)),
                ('required_speciality', models.CharField(choices=[('Neuro', 'Neuro'), ('Cardio', 'Cardio'), ('Pediatrics', 'Pediatrics')], default='Neuro', max_length=15)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
