# Generated by Django 5.0.4 on 2024-06-29 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ranch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('livestock_category', models.CharField(choices=[('terneros', 'Terneros'), ('terneras', 'Terneras'), ('novillos', 'Novillos'), ('vacas_de_invernada', 'Vacas de Invernada'), ('vaquillonas', 'Vaquillonas'), ('toros', 'Toros')], default='terneros', max_length=50)),
                ('cow_count', models.IntegerField(default=0)),
                ('ranch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranch.ranch')),
            ],
        ),
    ]
