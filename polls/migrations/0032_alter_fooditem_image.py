# Generated by Django 5.1.4 on 2025-01-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0031_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]