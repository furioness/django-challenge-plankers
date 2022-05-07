# Generated by Django 4.0.4 on 2022-05-07 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0006_generateddata_generation_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generateddata',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generated_data', to='schema.schema'),
        ),
    ]
