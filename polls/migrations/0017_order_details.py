# Generated by Django 5.1.4 on 2025-01-11 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_fooditem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
    ]