# Generated by Django 3.0.7 on 2020-07-02 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTaxe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=500, primary_key=True, serialize=False, unique=True)),
                ('img', models.CharField(max_length=300)),
                ('details', models.TextField()),
                ('ingredients', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductCategory')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductFamily')),
                ('taxe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductTaxe')),
            ],
        ),
    ]
