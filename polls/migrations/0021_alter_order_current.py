# Generated by Django 5.1.4 on 2025-01-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_order_confirm_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='current',
            field=models.CharField(choices=[('notdishpatched', 'notdishpatched'), ('dishpatched', 'dishpatched'), ('outfordel', 'outfordel'), ('deleivered', 'deleivered'), ('cancelled', 'cancelled')], default='notdishpatched', max_length=50),
        ),
    ]
