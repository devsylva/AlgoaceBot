# Generated by Django 5.1.4 on 2025-01-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_faq_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='profit',
            field=models.FloatField(default=0.0),
        ),
    ]
