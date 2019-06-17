# Generated by Django 2.1.8 on 2019-06-17 15:00

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20181205_1211'),
        ('hpaction', '0004_tenantchild'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPUser',
            fields=[
            ],
            options={
                'verbose_name': 'User HP Action',
                'proxy': True,
                'indexes': [],
            },
            bases=('users.justfixuser',),
            managers=[
                ('objects', users.models.JustfixUserManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='feewaiverdetails',
            options={'verbose_name': 'Fee waiver'},
        ),
        migrations.AlterModelOptions(
            name='tenantchild',
            options={'verbose_name_plural': 'Tenant children'},
        ),
    ]
