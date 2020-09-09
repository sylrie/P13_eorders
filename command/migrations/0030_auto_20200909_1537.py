# Generated by Django 3.1 on 2020-09-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('command', '0029_auto_20200906_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='status',
            field=models.CharField(choices=[('new', 'Nouvelle'), ('in-progress', 'en cours'), ('delivered', 'Livrée'), ('payed', 'Payée')], default='new', max_length=50),
        ),
    ]
