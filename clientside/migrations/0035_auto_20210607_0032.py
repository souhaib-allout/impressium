# Generated by Django 3.2.3 on 2021-06-06 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientside', '0034_auto_20210605_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pane',
            name='FileControle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FileControlePane', to='clientside.filecontrole'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='Quantity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='QuantityPane', to='clientside.quantity', verbose_name='Quantite'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='delevery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DeleveryPane', to='clientside.delivery'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='finition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FinitionPane', to='clientside.finition', verbose_name='Finition'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='fontColor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FontColorPane', to='clientside.fontcolor', verbose_name='Font coleur'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='formattype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FormaTypePane', to='clientside.formattype', verbose_name='Forma type'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='orientation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OrientationPane', to='clientside.orientation', verbose_name='Orientation'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='paperColor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PaperColorPane', to='clientside.papercolor', verbose_name='Papier coleur'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='paperType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PaperPane', to='clientside.papertype', verbose_name='Papier type'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='side',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SidePane', to='clientside.side', verbose_name='direction'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SizePane', to='clientside.size1', verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='pane',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserPane', to=settings.AUTH_USER_MODEL),
        ),
    ]
