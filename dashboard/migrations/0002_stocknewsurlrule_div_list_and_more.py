# Generated by Django 5.1.7 on 2025-04-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stocknewsurlrule",
            name="div_list",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="stocknewsurlrule",
            name="main_div",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="stocknewsurlrule",
            name="rows",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="stocknewsurlrule",
            name="tbody",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
