# Generated by Django 5.1.7 on 2025-04-04 03:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_alter_stocknewsurlrule_click_button"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stocknewsurlrule",
            name="click_button",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
