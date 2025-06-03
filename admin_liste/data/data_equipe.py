import psycopg2
import os

class Data_equipe:
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

    def get_all_equipe(self):

        sql = "SELECT * FROM equipe ORDER BY id_equipe;"

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
            print("Erreur get_all_equipe:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_1_equipe(self,type_rugby,genre,categorie_age):

        sql = "SELECT * FROM equipe WHERE (type_rugby,genre,categorie_age) =(%s,%s,%s);"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(type_rugby,genre,categorie_age)
            cursor.execute(sql,val)
            row = cursor.fetchone()


            return row
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