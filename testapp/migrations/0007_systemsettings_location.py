# Generated by Django 5.0 on 2024-02-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0006_alter_systemsettings_automate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsettings',
            name='location',
            field=models.CharField(choices=[('1', 'Kiambu01'), ('2', 'Kiambu02'), ('3', 'Thika01'), ('4', 'Thika02'), ('5', 'Online')], default='all', max_length=50),
        ),
    ]
