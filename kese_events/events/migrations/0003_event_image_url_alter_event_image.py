# Generated by Django 4.2.6 on 2023-10-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='event_images/'),
        ),
    ]
