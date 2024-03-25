import psycopg2

class Data_administrateur:

    def __init__(self):
        self._HOST = "localhost"
        self._DATABASE = "application_FFR_V5_db"
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


    def create_compte_administrateur(self,nom,prenom,mail,mot_de_passe,):

        sql = "INSERT INTO public.utilisateur(nom,prenom,mail,mot_de_passe,is_admin) VALUES (%s,%s,%s,%s,True) ON CONFLICT (mail,mot_de_passe) DO NOTHING;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(nom,prenom,mail,mot_de_passe)
            cursor.execute(sql,val)
            rows_affected = cursor.rowcount
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if rows_affected>0:
                print("Insertion reussie")
            else:
                print("La ligne existe déjà")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur create_compte")
            print(sql,val)
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def get_all_administrateur(self):
        sql = "SELECT * FROM utilisateur WHERE is_admin = True;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

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

    def update_compte_administrateur(self,nom,prenom,mail,mot_de_passe):

        sql = "UPDATE utilisateur SET mail=%s,mot_de_passe=%s WHERE nom = %s AND prenom = %s AND is_admin = True;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._HOST, database=self._DATABASE, user=self._USER, password=self._PASSWORD, port=self._PORT)
            # create a new cursor
            cursor = connection.cursor()
            val=(mail,mot_de_passe,nom,prenom)
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