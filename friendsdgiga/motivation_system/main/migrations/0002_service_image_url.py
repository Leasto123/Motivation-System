# Generated by Django 5.0.2 on 2024-06-07 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
