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



