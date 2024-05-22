# Generated by Django 5.0.6 on 2024-05-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0004_shortenedurl_expires_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="account_type",
            field=models.CharField(
                choices=[("free", "Free"), ("premium", "Premium")],
                default="free",
                max_length=10,
            ),
        ),
    ]
