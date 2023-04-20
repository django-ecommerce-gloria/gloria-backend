# Generated by Django 4.1.4 on 2023-02-13 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0009_remove_message_from_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='profile_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages_from', to='authuser.profile'),
        ),
    ]