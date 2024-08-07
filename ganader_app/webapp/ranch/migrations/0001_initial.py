# Generated by Django 5.0.4 on 2024-06-29 15:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_ranchs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RanchMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('ranch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='ranch.ranch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranch_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ranch')},
            },
        ),
        migrations.AddField(
            model_name='ranch',
            name='members',
            field=models.ManyToManyField(related_name='ranches', through='ranch.RanchMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]
