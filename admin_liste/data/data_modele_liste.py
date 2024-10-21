import psycopg2
import os

class DataModeleListe:
    def __init__(self):
        self._HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
        self._DATABASE = os.environ.get('POSTGRES_DB', 'application_ffr_db')
        self._USER = os.environ.get('POSTGRES_USER', 'dev')
        self._PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'ballon')
        self._PORT = int(os.environ.get('POSTGRES_PORT', 5432))

    def connect(self):
        """
        Fonction qui permet de valider la connexion à la base de données
        """
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)

            # obtentention d'un curseur, c'est à dire l'objet qui va recueillir les lignes en réponse des requêtes envoyées
            # au serveur de base de données
            cursor = connection.cursor()

            # exécution de la requête
            print('Version du serveur PostgreSQL:')
            cursor.execute('SELECT version()')

            # récupération des valeurs + affichage
            db_version = cursor.fetchone()
            print(db_version)


        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Connection à la base de données fermée.')

    def create_modele_liste(self,nom_modele_liste, type_rugby, nombre_joueurs_min, nombre_joueurs_max, duree_deplacement_min, duree_deplacement_max, nombre_match_min, nombre_match_max):

        sql = "INSERT INTO public.modele_liste(nom_modele_liste, type_rugby, nombre_joueurs_min, nombre_joueurs_max, duree_deplacement_min, duree_deplacement_max, nombre_match_min, nombre_match_max) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (type_rugby,nombre_joueurs_max, duree_deplacement_max, nombre_match_max) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val = (nom_modele_liste, type_rugby, nombre_joueurs_min, nombre_joueurs_max, duree_deplacement_min, duree_deplacement_max, nombre_match_min, nombre_match_max)
            cursor.execute(sql,val)
            rows_affected=cursor.rowcount

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Insertion reussie")
            else:
                print("La liste_depart existe déjà")


        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql,val)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def create_association_modele_liste_produit(self,id_modele_liste,id_produit,quantite_depart):

        sql = "INSERT INTO public.association_modele_liste_produit(id_modele_liste,id_produit,quantite_depart,quantite_retour) VALUES (%s,%s,%s,0) ON CONFLICT (id_modele_liste,id_produit) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_modele_liste,id_produit,quantite_depart)
            cursor.execute(sql,val)
            rows_affected=cursor.rowcount

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Insertion reussie")
            else:
                print("Le produit existe déjà dans cette liste")


        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql,val)
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def test_association_produit_liste(self,id_modele_liste,id_produit):

        sql = "SELECT id_association_modele_liste_produit FROM association_modele_liste_produit WHERE association_modele_liste_produit.id_modele_liste = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_modele_liste, id_produit)
            cursor.execute(sql, val)

            row=cursor.fetchone()

            if row:
                return True
            else:
                return False

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()



        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur update_liste_utilisateur")
            print(error)
        finally:
            if connection is not None:
                connection.close()



    def update_modele_liste(self,quantite_depart,id_modele_liste,id_produit):

        sql = "UPDATE association_modele_liste_produit SET quantite_depart=%s WHERE association_modele_liste_produit.id_modele_liste = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(quantite_depart,id_modele_liste, id_produit)
            cursor.execute(sql, val)


            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()



        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur update_liste_utilisateur")
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def delete_association_modele_liste_produit(self,id_modele_liste,id_produit):

        sql = "DELETE FROM association_modele_liste_produit WHERE (quantite_depart IS NULL OR quantite_depart = 0) AND id_modele_liste = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_modele_liste, id_produit)
            cursor.execute(sql, val)
            rows_affected = cursor.rowcount


            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Delete_produit_liste_depart ok")
            else:
                print("Delete_produit n'a pas marcher")


        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur delete_produit_liste_depart")
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def get_id_modele_liste(self,nom_modele_liste):

        sql = "SELECT * FROM modele_liste WHERE nom_modele_liste = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(nom_modele_liste,))
            row = cursor.fetchone()

            return row
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_id_multiples_parametres(self,type_rugby, nombre_joueurs_min, nombre_joueurs_max, duree_deplacement_min, duree_deplacement_max, nombre_match_min, nombre_match_max):

        sql = "SELECT * FROM modele_liste WHERE type_rugby = %s AND nombre_joueurs_min = %s AND nombre_joueurs_max = %s AND duree_deplacement_min = %s AND duree_deplacement_max = %s AND nombre_match_min = %s AND nombre_match_max = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(type_rugby, nombre_joueurs_min, nombre_joueurs_max, duree_deplacement_min, duree_deplacement_max, nombre_match_min, nombre_match_max,))
            row = cursor.fetchone()

            return row
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()




    def get_modele_liste(self,id_modele_liste):

        sql = "SELECT association_modele_liste_produit.id_modele_liste,stock.id_stock,stock.nom_stock,produit.id_produit,produit.nom_produit,association_modele_liste_produit.quantite_depart,association_modele_liste_produit.quantite_retour FROM association_modele_liste_produit JOIN produit ON association_modele_liste_produit.id_produit = produit.id_produit JOIN association_stock_produit ON association_stock_produit.id_produit=produit.id_produit JOIN stock ON stock.id_stock=association_stock_produit.id_stock WHERE association_modele_liste_produit.id_modele_liste = %s ORDER BY produit.id_produit;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_modele_liste,))
            rows = cursor.fetchall()

            return rows
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def test_exist(self,id_modele_liste):

        sql = "SELECT EXISTS (SELECT * FROM modele_liste WHERE id_modele_liste= %s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val = (id_modele_liste,)
            cursor.execute(sql,val)
            res = cursor.fetchone()

            return res
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur test_exist")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_all_modele_liste(self):

        sql = "SELECT * FROM modele_liste;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql)
            rows = cursor.fetchall()

            return rows
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()