# Generated by Django 3.0.8 on 2020-12-01 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_selection_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='selEnv', to='core.Events'),
        ),
    ]
