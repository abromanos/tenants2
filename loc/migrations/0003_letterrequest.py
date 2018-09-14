# Generated by Django 2.1 on 2018-09-13 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loc', '0002_landlorddetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetterRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mail_choice', models.TextField(choices=[('WE_WILL_MAIL', 'Yes, have JustFix.nyc mail this letter on my behalf.'), ('USER_WILL_MAIL', "No thanks, I'll mail it myself.")], help_text='How the letter of complaint will be mailed.', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='letter_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
