# Generated by Django 3.2.3 on 2021-06-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientside', '0043_commande_delevery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pane',
            name='ArticleDesign',
            field=models.FileField(null=True, upload_to='static/pane_images', verbose_name='Nom'),
        ),
    ]