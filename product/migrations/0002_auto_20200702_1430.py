# Generated by Django 3.0.7 on 2020-07-02 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit_price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='family',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductFamily'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='product',
            name='ingredients',
            field=models.TextField(blank=True),
        ),
    ]
