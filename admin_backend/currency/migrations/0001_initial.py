# Generated by Django 5.1.6 on 2025-04-11 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('currency_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('currency_name', models.CharField(max_length=255)),
                ('exchange_rate', models.DecimalField(decimal_places=6, max_digits=15)),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'db_table': 'currency',
                'managed': False,
            },
        ),
    ]
