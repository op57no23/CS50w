# Generated by Django 2.1.5 on 2019-10-29 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20191029_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='sicilian',
            field=models.BooleanField(default=False),
        ),
    ]
