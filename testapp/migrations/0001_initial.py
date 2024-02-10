# Generated by Django 5.0 on 2024-02-08 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='alert',
            fields=[
                ('alertid', models.AutoField(primary_key=True, serialize=False)),
                ('transactionid', models.CharField(max_length=20)),
                ('staffidi', models.CharField(max_length=30)),
                ('alert_status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='blacklist',
            fields=[
                ('blacklistid', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('transactionid', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='report',
            fields=[
                ('reportid', models.AutoField(default=3, primary_key=True, serialize=False)),
                ('transactionid', models.CharField(max_length=20)),
                ('staffid', models.CharField(max_length=40)),
                ('report_status', models.CharField(max_length=30)),
                ('verification', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('transactionid', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=30)),
                ('transaction_data', models.CharField(max_length=3000)),
                ('transaction_state', models.CharField(default='incoming', max_length=11)),
            ],
        ),
    ]
