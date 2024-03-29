# Generated by Django 3.2.3 on 2021-06-04 20:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientside', '0026_article_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('price', models.FloatField(verbose_name='Prix')),
                ('mindays', models.IntegerField(verbose_name='Minimun de nb de jours')),
                ('maxdays', models.IntegerField(verbose_name='Maximun de nb de jours')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
