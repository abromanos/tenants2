# Generated by Django 2.1.2 on 2018-10-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0006_auto_20181004_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landlorddetails',
            name='lookup_date',
            field=models.DateField(blank=True, help_text="When we last tried to look up the landlord's details.", null=True),
        ),
    ]
