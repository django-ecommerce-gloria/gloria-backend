# Generated by Django 4.1.4 on 2023-03-24 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]