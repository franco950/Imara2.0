# Generated by Django 5.0 on 2024-03-10 00:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0015_alter_alert_timestamp_alter_report_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 10, 3, 26, 15, 879943, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='report',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 10, 3, 26, 15, 879943, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 10, 3, 26, 15, 878938, tzinfo=datetime.timezone.utc)),
        ),
    ]
