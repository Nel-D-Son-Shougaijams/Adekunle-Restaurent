# Generated by Django 5.1.4 on 2025-01-07 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.JSONField(default=dict),
        ),
    ]
