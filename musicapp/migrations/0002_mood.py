# Generated by Django 4.0.4 on 2022-04-27 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_name', models.CharField(max_length=200)),
                ('artist_name', models.CharField(max_length=200)),
                ('mood', models.CharField(max_length=200)),
            ],
        ),
    ]
