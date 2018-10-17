# Generated by Django 2.1.2 on 2018-10-17 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0003_auto_20181004_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboardinginfo',
            name='zipcode',
            field=models.CharField(blank=True, help_text="The user's ZIP code. This field is automatically updated when you change the address or borough, so you generally shouldn't have to change it manually.", max_length=12),
        ),
    ]
