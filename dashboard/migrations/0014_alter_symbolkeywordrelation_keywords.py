# Generated by Django 5.1.7 on 2025-04-07 06:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0013_alter_symbolkeywordrelation_keywords"),
    ]

    operations = [
        migrations.AlterField(
            model_name="symbolkeywordrelation",
            name="keywords",
            field=models.ManyToManyField(
                blank=True, related_name="news_keywords", to="dashboard.keyword"
            ),
        ),
    ]
