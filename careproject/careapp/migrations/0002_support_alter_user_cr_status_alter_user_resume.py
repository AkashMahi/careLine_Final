# Generated by Django 4.2 on 2023-04-17 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='cr_status',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='resume',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]