import psycopg2

class Data_deplacement:
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


    def create_deplacement(self,nombre_joueurs,duree_deplacement,nombre_match):

        sql = "INSERT INTO public.deplacement(nombre_joueurs,duree_deplacement,nombre_match) VALUES (%s,%s,%s) ON CONFLICT (nombre_joueurs,duree_deplacement,nombre_match) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nombre_joueurs,duree_deplacement,nombre_match)
            cursor.execute(sql,val)
            rows_affected = cursor.rowcount
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Insertion reussie")
            else:
                print("Le deplacement existe deja")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql,val)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def update_deplacement(self,nombre_joueurs,duree_deplacement,nombre_match):

        sql = "UPDATE public.deplacement SET nombre_joueurs = %s ,duree_deplacement = %s ,nombre_match = %s) WHERE nombre_joueurs=%s AND duree_deplacement = %s AND nombre_match=%s;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nombre_joueurs,duree_deplacement,nombre_match)
            cursor.execute(sql,val)
            rows_affected = cursor.rowcount
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Modification reussie")
            else:
                print("Le deplacement n'existe pas")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur update_liste")
            print(sql,val)
            print(error)
        finally:
            if connection is not None:
                connection.close()



    def get_all_deplacement(self):

        sql = "SELECT * FROM deplacement;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            cursor.execute(sql)
            rows=cursor.fetchall()
            for row in rows:
                print(row)
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_all_deplacement")
            print(sql)
            print(error)
        finally:
            if connection is not None:
                connection.close()




    def get_1_deplacement(self,nombre_joueurs,duree_deplacement,nombre_match):

        sql = "SELECT * FROM deplacement WHERE (nombre_joueurs,duree_deplacement,nombre_match) = (%s,%s,%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nombre_joueurs,duree_deplacement,nombre_match)
            cursor.execute(sql,val)
            row=cursor.fetchone()
            print(row)
            return(row)
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_liste")
            print(sql,val)
            print(error)
        finally:
            if connection is not None:
                connection.close()
