# Generated by Django 3.1 on 2020-08-24 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('command', '0020_bill_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='amount',
        ),
    ]