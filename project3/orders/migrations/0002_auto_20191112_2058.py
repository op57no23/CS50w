# Generated by Django 2.1.5 on 2019-11-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='large_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='small_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
