# Generated by Django 4.2 on 2023-06-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careapp', '0006_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='c_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='p_id',
            field=models.IntegerField(),
        ),
    ]