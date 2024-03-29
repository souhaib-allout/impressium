# Generated by Django 3.2.3 on 2021-06-05 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientside', '0027_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='pane',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='UserPane', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pane',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ArticlePane', to='clientside.article'),
        ),
    ]
