import psycopg2

class Data_liste_utilisateur:
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

    def create_liste_utilisateur(self,id_utilisateur,id_liste_depart,date_liste,destination):

        sql = "INSERT INTO public.liste_utilisateur(id_utilisateur,id_liste_depart,date_liste,destination,en_cours) VALUES (%s,%s,%s,%s,TRUE) ON CONFLICT (id_utilisateur,id_liste_depart,date_liste) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_utilisateur,id_liste_depart,date_liste,destination)
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
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def create_association_liste_utilisateur_produit(self,id_liste_utilisateur,id_liste_depart):

        sql = "INSERT INTO public.association_liste_utilisateur_produit(id_liste_utilisateur,id_produit,quantite_depart,quantite_retour) SELECT %s, association_liste_depart_produit.id_produit,association_liste_depart_produit.quantite_depart,association_liste_depart_produit.quantite_retour FROM association_liste_depart_produit WHERE id_liste_depart = %s ON CONFLICT (id_liste_utilisateur,id_produit) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_liste_utilisateur,id_liste_depart)
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
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_id_liste_utilisateur(self,id_utilisateur,id_liste_depart,date_liste):

        sql = "SELECT * FROM liste_utilisateur WHERE (id_utilisateur,id_liste_depart,date_liste) = (%s,%s,%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_utilisateur,id_liste_depart,date_liste))
            row = cursor.fetchone()
            print(row)
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

    def get_all_liste_utilisateur(self,id_utilisateur):

        sql = "SELECT * FROM liste_utilisateur WHERE id_utilisateur = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_utilisateur,))
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

    def get_liste_utilisateur(self,id_liste_utilisateur):

        sql = "SELECT association_liste_utilisateur_produit.id_liste_utilisateur,stock.id_stock,stock.nom_stock,produit.id_produit,produit.nom_produit,association_liste_utilisateur_produit.quantite_depart,association_liste_utilisateur_produit.quantite_retour FROM association_liste_utilisateur_produit JOIN produit ON association_liste_utilisateur_produit.id_produit = produit.id_produit JOIN association_stock_produit ON association_stock_produit.id_produit=produit.id_produit JOIN stock ON stock.id_stock=association_stock_produit.id_stock WHERE association_liste_utilisateur_produit.id_liste_utilisateur = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_liste_utilisateur,))
            rows = cursor.fetchall()

            return rows
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_liste")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def update_liste_utilisateur(self,quantite_retour,id_liste_utilisateur,id_produit):

        sql = "UPDATE association_liste_utilisateur_produit SET quantite_retour=%s WHERE association_liste_utilisateur_produit.id_liste_utilisateur = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(quantite_retour,id_liste_utilisateur, id_produit)
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

    def get_id_liste_utilisateur_en_cours(self,id_utilisateur):

        sql = "SELECT * FROM liste_utilisateur WHERE (id_utilisateur,en_cours) = (%s,True);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_utilisateur,))
            row = cursor.fetchone()
            print(row)
            return row
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_liste_utilisateur_en_cours")
            print(sql)
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
