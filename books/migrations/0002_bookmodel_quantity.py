# Generated by Django 5.0.6 on 2024-07-03 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='quantity',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
