# Generated by Django 3.1 on 2020-08-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('command', '0014_auto_20200821_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='price',
            field=models.FloatField(),
            preserve_default=False,
        ),
    ]
