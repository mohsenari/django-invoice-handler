# Generated by Django 2.2 on 2019-05-09 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_auto_20190509_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]