# Generated by Django 5.1.6 on 2025-02-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("certifications", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="certification",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="certification_logos/"
            ),
        ),
    ]
