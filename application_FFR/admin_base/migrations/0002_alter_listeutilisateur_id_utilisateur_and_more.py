# Generated by Django 5.0.2 on 2024-03-08 14:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='listeutilisateur',
            name='id_utilisateur',
            field=models.ForeignKey(blank=True, db_column='id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelOptions(
            name='associationstockproduit',
            options={'managed': True, 'verbose_name_plural': 'Mettre à jour le stock'},
        ),
        migrations.AlterModelOptions(
            name='produit',
            options={'managed': True, 'verbose_name_plural': 'Ajouter un nouveau produit'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'managed': True, 'verbose_name_plural': 'Ajouter un nouveau stock'},
        ),
        migrations.DeleteModel(
            name='Utilisateur',
        ),
    ]
