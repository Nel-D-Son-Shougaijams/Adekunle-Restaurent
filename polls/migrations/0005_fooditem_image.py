# Generated by Django 5.1.4 on 2025-01-08 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_fooditem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='static/random-foods.jpg', upload_to=''),
        ),
    ]