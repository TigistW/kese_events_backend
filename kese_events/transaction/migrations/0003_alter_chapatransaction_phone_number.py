# Generated by Django 4.2.6 on 2023-10-18 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_chapatransaction_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapatransaction',
            name='phone_number',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
