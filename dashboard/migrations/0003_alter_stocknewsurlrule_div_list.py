# Generated by Django 5.1.7 on 2025-04-04 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_stocknewsurlrule_div_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocknewsurlrule',
            name='div_list',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
