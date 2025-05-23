# Generated by Django 5.1.6 on 2025-04-18 05:47

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
            name='AuditLog',
            fields=[
                ('log_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('action', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': '"admin"."audit_log"',
            },
        ),
    ]
