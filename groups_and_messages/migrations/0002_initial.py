# Generated by Django 4.2 on 2024-09-07 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups_and_messages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='seen_list',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='users who saw this message'),
        ),
        migrations.AddField(
            model_name='chat_messages',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups_and_messages.chat_group', verbose_name='parent group of message'),
        ),
        migrations.AddField(
            model_name='chat_messages',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='the use who sent this message'),
        ),
        migrations.AddField(
            model_name='chat_group',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="group's users"),
        ),
    ]
