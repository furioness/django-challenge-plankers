# Generated by Django 4.0.4 on 2022-05-09 11:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0009_remove_generateddata_generation_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='generateddata',
            name='created',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
