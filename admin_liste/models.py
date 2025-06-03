from django.db import models
from admin_stock.models import Produit
from django.contrib.auth.models import User

class AssociationModeleListeProduit(models.Model):
    id_association_modele_liste_produit = models.SmallAutoField(primary_key=True)
    id_modele_liste = models.ForeignKey('ModeleListe', models.DO_NOTHING, db_column='id_modele_liste', blank=True, null=True)
    id_produit = models.ForeignKey(Produit, models.DO_NOTHING, db_column='id_produit', blank=True, null=True)
    quantite_depart = models.SmallIntegerField(blank=True, null=True)
    quantite_retour = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'association_modele_liste_produit'
        unique_together = (('id_modele_liste', 'id_produit'),)

    def __str__(self):
        return f"Association {self.id_modele_liste} - {self.id_produit}"

class AssociationListeUtilisateurProduit(models.Model):
    id_association_liste_utilisateur_produit = models.SmallAutoField(primary_key=True)
    id_liste_utilisateur = models.ForeignKey('ListeUtilisateur', models.DO_NOTHING, db_column='id_liste_utilisateur', blank=True, null=True)
    id_produit = models.ForeignKey(Produit, models.DO_NOTHING, db_column='id_produit', blank=True, null=True)
    quantite_depart = models.SmallIntegerField(blank=True, null=True)
    quantite_retour = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'association_liste_utilisateur_produit'
        unique_together = (('id_liste_utilisateur', 'id_produit'),)

    def __str__(self):
        return f"Association {self.id_liste_utilisateur} - {self.id_produit}"

class Equipe(models.Model):
    id_equipe = models.SmallAutoField(primary_key=True)
    type_rugby = models.SmallIntegerField(blank=True, null=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    categorie_age = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'equipe'

    def __str__(self):
        return f"Equipe {self.id_equipe} - {self.type_rugby} - {self.genre} - {self.categorie_age}"

class ModeleListe(models.Model):
    id_modele_liste = models.SmallAutoField(primary_key=True)
    nom_modele_liste = models.CharField(max_length=20, blank=True, null=True, unique=True)
    id_equipe = models.ForeignKey(Equipe, models.DO_NOTHING, db_column='id_equipe', blank=True, null=True)
    nombre_joueurs_min = models.SmallIntegerField(blank=True, null=True)
    nombre_joueurs_max = models.SmallIntegerField(blank=True, null=True)
    duree_deplacement_min = models.SmallIntegerField(blank=True, null=True)
    duree_deplacement_max = models.SmallIntegerField(blank=True, null=True)
    nombre_match = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'modele_liste'
        unique_together = (('id_equipe', 'nombre_joueurs_max','duree_deplacement_max','nombre_match'),)

    def __str__(self):
        return self.nom_modele_liste or f"ModeleListe {self.id_modele_liste}"

class ListeUtilisateur(models.Model):
    id_liste_utilisateur = models.SmallAutoField(primary_key=True)
    id_utilisateur = models.ForeignKey(User, models.DO_NOTHING, db_column='id_utilisateur', blank=True, null=True)
    id_equipe = models.ForeignKey(Equipe, models.DO_NOTHING, db_column='id_equipe', blank=True, null=True)
    id_modele_liste = models.ForeignKey(ModeleListe, models.DO_NOTHING, db_column='id_modele_liste', blank=True, null=True)
    nombre_joueurs = models.SmallIntegerField(blank=True, null=True)
    duree_deplacement = models.SmallIntegerField(blank=True, null=True)
    nombre_match = models.SmallIntegerField(blank=True, null=True)
    date_liste = models.DateField(blank=True, null=True)
    destination = models.CharField(max_length=30, blank=True, null=True)
    statut = models.CharField(max_length=20, blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'liste_utilisateur'
        unique_together = (('id_utilisateur', 'id_modele_liste', 'date_liste'),)

    def __str__(self):
        return f"Liste de {self.id_utilisateur} - {self.date_liste}"