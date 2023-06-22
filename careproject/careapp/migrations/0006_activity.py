# Generated by Django 4.2 on 2023-06-15 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('careapp', '0005_remove_user_cr_dist1_remove_user_cr_dist2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(max_length=45)),
                ('astatus', models.CharField(max_length=20)),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caretaker_id', to=settings.AUTH_USER_MODEL)),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
