# Generated by Django 2.1.5 on 2019-10-24 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='top_number',
        ),
    ]