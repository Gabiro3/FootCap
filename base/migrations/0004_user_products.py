# Generated by Django 4.2.7 on 2023-11-07 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='products',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
