# Generated by Django 5.0 on 2024-03-17 15:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0024_alter_alert_timestamp_alter_report_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 17, 18, 56, 17, 682416, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='report',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 17, 18, 56, 17, 683393, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 17, 18, 56, 17, 682416, tzinfo=datetime.timezone.utc)),
        ),
    ]
