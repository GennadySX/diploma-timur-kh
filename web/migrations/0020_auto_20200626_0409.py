# Generated by Django 3.0.7 on 2020-06-26 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_auto_20200626_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='group',
            field=models.CharField(choices=[('сухие смеси и грунтовки', 'сухие смеси и грунтовки'), ('Облицовочные материалы', 'Облицовочные материалы'), ('Изоляционные материалы', 'Изоляционные материалы'), ('Листовые материалы', 'Листовые материалы')], default='сухие смеси и грунтовки', max_length=50),
        ),
    ]