# Generated by Django 3.0.7 on 2020-06-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20200621_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='group',
            field=models.CharField(choices=[('mobile', 'mobile'), ('accessories', 'accessories'), ('pc', 'pc'), ('notebook', 'notebook')], default='mobile', max_length=20),
        ),
    ]
