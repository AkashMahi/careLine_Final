# Generated by Django 4.2 on 2023-06-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careapp', '0012_activity_duration_alter_activity_aname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='dept',
            field=models.IntegerField(null=True),
        ),
    ]
