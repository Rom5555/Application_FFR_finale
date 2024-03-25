# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User



class AssociationListeDepartProduit(models.Model):
    id_association_liste_depart_produit = models.SmallAutoField(primary_key=True)
    id_liste_depart = models.ForeignKey('ListeDepart', models.DO_NOTHING, db_column='id_liste_depart', blank=True, null=True)
    id_produit = models.ForeignKey('Produit', models.DO_NOTHING, db_column='id_produit', blank=True, null=True)
    quantite_depart = models.SmallIntegerField(blank=True, null=True)
    quantite_retour = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'association_liste_depart_produit'
        unique_together = (('id_liste_depart', 'id_produit'),)


class AssociationListeUtilisateurProduit(models.Model):
    id_association_liste_utilisateur_produit = models.SmallAutoField(primary_key=True)
    id_liste_utilisateur = models.ForeignKey('ListeUtilisateur', models.DO_NOTHING, db_column='id_liste_utilisateur', blank=True, null=True)
    id_produit = models.ForeignKey('Produit', models.DO_NOTHING, db_column='id_produit', blank=True, null=True)
    quantite_depart = models.SmallIntegerField(blank=True, null=True)
    quantite_retour = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'association_liste_utilisateur_produit'
        unique_together = (('id_liste_utilisateur', 'id_produit'),)


class AssociationStockProduit(models.Model):
    id_association_stock_produit = models.SmallAutoField(primary_key=True)
    id_stock = models.ForeignKey('Stock', models.DO_NOTHING, db_column='id_stock', blank=True, null=True)
    id_produit = models.ForeignKey('Produit', models.DO_NOTHING, db_column='id_produit', blank=True, null=True)
    quantite = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.id_produit.nom_produit}'

    class Meta:
        managed = True
        db_table = 'association_stock_produit'
        verbose_name_plural = 'Mettre à jour le stock'

class CategorieProduit(models.Model):
    id_categorie_produit = models.SmallAutoField(primary_key=True)
    nom_categorie_produit = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'categorie_produit'


class Deplacement(models.Model):
    id_deplacement = models.SmallAutoField(primary_key=True)
    nombre_joueurs = models.SmallIntegerField(blank=True, null=True)
    duree_deplacement = models.SmallIntegerField(blank=True, null=True)
    nombre_match = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'deplacement'
        unique_together = (('nombre_joueurs', 'duree_deplacement', 'nombre_match'),)


class Equipe(models.Model):
    id_equipe = models.SmallAutoField(primary_key=True)
    type_rugby = models.SmallIntegerField(blank=True, null=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    categorie_age = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'equipe'


class ListeDepart(models.Model):
    id_liste_depart = models.SmallAutoField(primary_key=True)
    id_deplacement = models.ForeignKey(Deplacement, models.DO_NOTHING, db_column='id_deplacement', blank=True, null=True)
    id_equipe = models.ForeignKey(Equipe, models.DO_NOTHING, db_column='id_equipe', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'liste_depart'
        unique_together = (('id_deplacement', 'id_equipe'),)


class ListeUtilisateur(models.Model):
    id_liste_utilisateur = models.SmallAutoField(primary_key=True)
    id_utilisateur = models.ForeignKey(User, models.DO_NOTHING, db_column='id', blank=True, null=True)
    id_liste_depart = models.ForeignKey(ListeDepart, models.DO_NOTHING, db_column='id_liste_depart', blank=True, null=True)
    date_liste = models.DateField(blank=True, null=True)
    destination = models.CharField(max_length=30, blank=True, null=True)
    en_cours = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'liste_utilisateur'
        unique_together = (('id_utilisateur', 'id_liste_depart', 'date_liste'),)


class Produit(models.Model):
    id_produit = models.SmallAutoField(primary_key=True)
    nom_produit = models.CharField(unique=True, max_length=50, blank=True, null=True)
    id_categorie_produit = models.ForeignKey(CategorieProduit, models.DO_NOTHING, db_column='id_categorie_produit', blank=True, null=True)

    def __str__(self):
        return self.nom_produit

    class Meta:
        managed = True
        db_table = 'produit'
        verbose_name_plural = 'Ajouter un nouveau produit'

class Stock(models.Model):
    id_stock = models.SmallAutoField(primary_key=True)
    nom_stock = models.CharField(unique=True, max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nom_stock

    class Meta:
        managed = True
        db_table = 'stock'
        verbose_name_plural = 'Ajouter un nouveau stock'


