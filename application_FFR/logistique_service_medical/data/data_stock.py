import psycopg2

class Data_stock:
    def __init__(self):
        self._HOST = "localhost"
        self._DATABASE = "django_FFR_db"
        self._USER = "dev"
        self._PASSWORD = "ballon"
        self._PORT = 5432

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




    def get_all_stocks(self):
        sql = "SELECT * FROM stock ORDER BY id_stock;"

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

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_stock_item:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_all_produits(self):
        sql = "SELECT * FROM produit ORDER BY id_produit;"

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

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_stock_item:")
            print(error)
        finally:
            if connection is not None:
                connection.close()



    def get_stock_consommable(self):
        sql = "SELECT stock.id_stock,stock.nom_stock,produit.id_produit,produit.nom_produit,association_stock_produit.quantite FROM association_stock_produit JOIN produit ON association_stock_produit.id_produit = produit.id_produit JOIN stock ON association_stock_produit.id_stock = stock.id_stock WHERE association_stock_produit.id_stock = 1 ORDER BY id_produit;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql)
            count= cursor.rowcount
            rows = cursor.fetchall()

            return count,rows
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_stock_item:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_1_stock(self, id_stock):
        sql = "SELECT stock.id_stock, stock.nom_stock, produit.id_produit, produit.nom_produit, association_stock_produit.quantite " \
              "FROM association_stock_produit " \
              "JOIN produit ON association_stock_produit.id_produit = produit.id_produit " \
              "JOIN stock ON association_stock_produit.id_stock = stock.id_stock " \
              "WHERE association_stock_produit.id_stock = %s " \
              "ORDER BY produit.id_produit;"

        connection = None
        try:
            # Obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER,
                                          password=self._PASSWORD, port=self._PORT)
            # Création d'un nouveau curseur
            cursor = connection.cursor()

            cursor.execute(sql, (id_stock,))
            count = cursor.rowcount
            rows = cursor.fetchall()

            return count, rows

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_stock_consommable:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_id_stock(self,nom):
        sql = "SELECT id_stock,nom FROM stock WHERE nom = %s ;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(nom,))

            row = cursor.fetchone()

            return row
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_stock_item:")
            print(error)
        finally:
            if connection is not None:
                connection.close()



    def get_stock_1produit(self,id_produit):

        sql = "SELECT stock.id_stock,stock.nom_stock,produit.id_produit,produit.nom_produit,association_stock_produit.quantite FROM association_stock_produit JOIN produit ON association_stock_produit.id_produit = produit.id_produit JOIN stock ON association_stock_produit.id_stock = stock.id_stock WHERE produit.id_produit = {0};".format(id_produit)

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, id_produit)

            row = cursor.fetchone()
            return row

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_stock_item:")
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def get_1_produit(self,premieres_lettres):


        sql = "SELECT * FROM produit WHERE LOWER(nom_produit) LIKE %s ORDER BY id_produit;"
        args=[premieres_lettres+'%']

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            cursor.execute(sql, args)

            rows = cursor.fetchall()

            return rows


            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur recherche_nom_produit")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def ajouter_quantite_stock(self,nombre_ajoute,id_produit):

        sql = "UPDATE association_stock_produit SET quantite=quantite+(%s) WHERE id_produit = (%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nombre_ajoute, id_produit)
            cursor.execute(sql, val)


            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()



        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur update_stock")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def retirer_quantite_stock(self,nombre_retire,id_produit):

        sql = "UPDATE association_stock_produit SET quantite=quantite-(%s) WHERE id_produit = (%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nombre_retire, id_produit)
            cursor.execute(sql, val)
            rows_affected = cursor.rowcount

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected > 0:
                print("Insertion reussie")
            else:
                print("La quantité de produit n'a pas pu être mise à jour")


        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur update_stock")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def add_produit_stock(self,nom,id_stock, quantite):


        sql = "WITH nouveau_produit AS (INSERT INTO produit(nom_produit) VALUES(%s) ON CONFLICT (nom_produit) DO NOTHING RETURNING id_produit) INSERT INTO association_stock_produit(id_stock,id_produit,quantite) SELECT %s,id_produit,%s FROM nouveau_produit;"



        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, (nom,id_stock,quantite))
            rows_affected=cursor.rowcount
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Insertion reussie")
            else:
                print("La ligne existe déjà")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur ajout_consommable")
            print(sql)
            print(nom)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def delete_produit_stock(self, id_produit):
        sql = """
        DELETE FROM association_stock_produit 
        WHERE id_produit = %s;

        DELETE FROM produit 
        WHERE id_produit = %s;
        """

        connection = None
        try:
            # Obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER,
                                          password=self._PASSWORD, port=self._PORT)
            # Création d'un nouveau curseur
            cursor = connection.cursor()

            cursor.execute(sql, (id_produit, id_produit))
            rows_affected = cursor.rowcount
            # Validation des changements dans la base de données
            connection.commit()
            # Fermeture de la communication avec la base de données
            cursor.close()

            if rows_affected > 0:
                print("Suppression réussie")
            else:
                print("Aucune ligne correspondante trouvée pour la suppression")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur lors de la suppression de produit dans le stock")
            print(sql)
            print(id_produit)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def update_quantity(self,nouvelle_quantite,id_produit):

        sql = "UPDATE association_stock_produit SET quantite=(%s) WHERE id_produit = (%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nouvelle_quantite, id_produit)
            cursor.execute(sql, val)

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur update_stock")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def valider_liste_retour(self, id_liste_utilisateur):

        sql = "UPDATE liste_utilisateur SET en_cours = False WHERE id_liste_utilisateur = (%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER,
                                          password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, (id_liste_utilisateur,))

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur validation liste retour")
            print(error)
        finally:
            if connection is not None:
                connection.close()

