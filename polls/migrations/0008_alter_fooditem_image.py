# Generated by Django 5.1.4 on 2025-01-10 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_fooditem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='//static/random-foods.jpg', upload_to=''),
        ),
    ]
