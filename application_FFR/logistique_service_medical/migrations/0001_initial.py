# Generated by Django 5.0.2 on 2024-03-01 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieProduit',
            fields=[
                ('id_categorie_produit', models.SmallAutoField(primary_key=True, serialize=False)),
                ('nom_categorie_produit', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'categorie_produit',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id_equipe', models.SmallAutoField(primary_key=True, serialize=False)),
                ('type_rugby', models.SmallIntegerField(blank=True, null=True)),
                ('genre', models.CharField(blank=True, max_length=10, null=True)),
                ('categorie_age', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'equipe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id_stock', models.SmallAutoField(primary_key=True, serialize=False)),
                ('nom_stock', models.CharField(blank=True, max_length=50, null=True, unique=True)),
            ],
            options={
                'db_table': 'stock',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Deplacement',
            fields=[
                ('id_deplacement', models.SmallAutoField(primary_key=True, serialize=False)),
                ('nombre_joueurs', models.SmallIntegerField(blank=True, null=True)),
                ('duree_deplacement', models.SmallIntegerField(blank=True, null=True)),
                ('nombre_match', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'deplacement',
                'managed': True,
                'unique_together': {('nombre_joueurs', 'duree_deplacement', 'nombre_match')},
            },
        ),
        migrations.CreateModel(
            name='ListeDepart',
            fields=[
                ('id_liste_depart', models.SmallAutoField(primary_key=True, serialize=False)),
                ('id_deplacement', models.ForeignKey(blank=True, db_column='id_deplacement', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.deplacement')),
                ('id_equipe', models.ForeignKey(blank=True, db_column='id_equipe', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.equipe')),
            ],
            options={
                'db_table': 'liste_depart',
                'managed': True,
                'unique_together': {('id_deplacement', 'id_equipe')},
            },
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id_produit', models.SmallAutoField(primary_key=True, serialize=False)),
                ('nom_produit', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('id_categorie_produit', models.ForeignKey(blank=True, db_column='id_categorie_produit', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.categorieproduit')),
            ],
            options={
                'db_table': 'produit',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AssociationStockProduit',
            fields=[
                ('id_association_stock_produit', models.SmallAutoField(primary_key=True, serialize=False)),
                ('quantite', models.SmallIntegerField(blank=True, null=True)),
                ('id_produit', models.ForeignKey(blank=True, db_column='id_produit', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.produit')),
                ('id_stock', models.ForeignKey(blank=True, db_column='id_stock', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.stock')),
            ],
            options={
                'db_table': 'association_stock_produit',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id_utilisateur', models.SmallAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, max_length=20, null=True)),
                ('prenom', models.CharField(blank=True, max_length=20, null=True)),
                ('mail', models.CharField(blank=True, max_length=30, null=True)),
                ('mot_de_passe', models.CharField(blank=True, max_length=15, null=True)),
                ('is_admin', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'utilisateur',
                'managed': True,
                'unique_together': {('mail', 'mot_de_passe')},
            },
        ),
        migrations.CreateModel(
            name='ListeUtilisateur',
            fields=[
                ('id_liste_utilisateur', models.SmallAutoField(primary_key=True, serialize=False)),
                ('date_liste', models.DateField(blank=True, null=True)),
                ('destination', models.CharField(blank=True, max_length=30, null=True)),
                ('en_cours', models.BooleanField(blank=True, null=True)),
                ('id_liste_depart', models.ForeignKey(blank=True, db_column='id_liste_depart', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.listedepart')),
                ('id_utilisateur', models.ForeignKey(blank=True, db_column='id_utilisateur', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.utilisateur')),
            ],
            options={
                'db_table': 'liste_utilisateur',
                'managed': True,
                'unique_together': {('id_utilisateur', 'id_liste_depart', 'date_liste')},
            },
        ),
        migrations.CreateModel(
            name='AssociationListeUtilisateurProduit',
            fields=[
                ('id_association_liste_utilisateur_produit', models.SmallAutoField(primary_key=True, serialize=False)),
                ('quantite_depart', models.SmallIntegerField(blank=True, null=True)),
                ('quantite_retour', models.SmallIntegerField(blank=True, null=True)),
                ('id_liste_utilisateur', models.ForeignKey(blank=True, db_column='id_liste_utilisateur', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.listeutilisateur')),
                ('id_produit', models.ForeignKey(blank=True, db_column='id_produit', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.produit')),
            ],
            options={
                'db_table': 'association_liste_utilisateur_produit',
                'managed': True,
                'unique_together': {('id_liste_utilisateur', 'id_produit')},
            },
        ),
        migrations.CreateModel(
            name='AssociationListeDepartProduit',
            fields=[
                ('id_association_liste_depart_produit', models.SmallAutoField(primary_key=True, serialize=False)),
                ('quantite_depart', models.SmallIntegerField(blank=True, null=True)),
                ('quantite_retour', models.SmallIntegerField(blank=True, null=True)),
                ('id_liste_depart', models.ForeignKey(blank=True, db_column='id_liste_depart', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.listedepart')),
                ('id_produit', models.ForeignKey(blank=True, db_column='id_produit', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='logistique_service_medical.produit')),
            ],
            options={
                'db_table': 'association_liste_depart_produit',
                'managed': True,
                'unique_together': {('id_liste_depart', 'id_produit')},
            },
        ),
    ]
