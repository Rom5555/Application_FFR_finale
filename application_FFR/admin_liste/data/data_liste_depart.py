import psycopg2

class Data_liste_depart:
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

    def create_liste_depart(self,id_equipe,id_deplacement):

        sql = "INSERT INTO public.liste_depart(id_equipe,id_deplacement) VALUES (%s,%s) ON CONFLICT (id_equipe,id_deplacement) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_equipe,id_deplacement)
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

    def create_association_liste_depart_produit(self,id_liste_depart,id_produit,quantite_depart):

        sql = "INSERT INTO public.association_liste_depart_produit(id_liste_depart,id_produit,quantite_depart,quantite_retour) VALUES (%s,%s,%s,0) ON CONFLICT (id_liste_depart,id_produit) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_liste_depart,id_produit,quantite_depart)
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


    def test_association_produit_liste(self,id_liste_depart,id_produit):

        sql = "SELECT id_association_liste_depart_produit FROM association_liste_depart_produit WHERE association_liste_depart_produit.id_liste_depart = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_liste_depart, id_produit)
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



    def update_liste_depart(self,quantite_depart,id_liste_depart,id_produit):

        sql = "UPDATE association_liste_depart_produit SET quantite_depart=%s WHERE association_liste_depart_produit.id_liste_depart = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(quantite_depart,id_liste_depart, id_produit)
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


    def delete_association_liste_depart_produit(self,id_liste_depart,id_produit):

        sql = "DELETE FROM association_liste_depart_produit WHERE (quantite_depart IS NULL OR quantite_depart = 0) AND id_liste_depart = %s AND id_produit = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(id_liste_depart, id_produit)
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


    def get_id_liste_depart(self,id_equipe,id_deplacement):

        sql = "SELECT * FROM liste_depart WHERE (id_equipe,id_deplacement) = (%s,%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_equipe,id_deplacement))
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

    def get_liste_depart(self,id_liste_depart):

        sql = "SELECT association_liste_depart_produit.id_liste_depart,stock.id_stock,stock.nom_stock,produit.id_produit,produit.nom_produit,association_liste_depart_produit.quantite_depart,association_liste_depart_produit.quantite_retour FROM association_liste_depart_produit JOIN produit ON association_liste_depart_produit.id_produit = produit.id_produit JOIN association_stock_produit ON association_stock_produit.id_produit=produit.id_produit JOIN stock ON stock.id_stock=association_stock_produit.id_stock WHERE association_liste_depart_produit.id_liste_depart = %s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql,(id_liste_depart,))
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

    def test_exist(self,id_equipe,id_deplacement):

        sql = "SELECT EXISTS (SELECT 1 FROM liste_depart WHERE id_equipe = %s AND id_deplacement = %s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val = (id_equipe,id_deplacement)
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

    def get_all_liste_depart(self):

        sql = "SELECT liste_depart.id_liste_depart,equipe.type_rugby,equipe.genre,equipe.categorie_age,deplacement.nombre_joueurs,deplacement.duree_deplacement FROM liste_depart JOIN equipe ON liste_depart.id_equipe = equipe.id_equipe JOIN deplacement ON liste_depart.id_deplacement=deplacement.id_deplacement;"

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