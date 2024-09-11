import os

if __name__ == '__main__':

    # adapter les valeurs en rapport avec la configuration de votre environnement
    # de développement
    SERVER = "165.22.65.214"
    PORT = 5432
    USER = "rom"
    PASSWORD = "ballon"
    SCRIPTS_DIRECTORY = "C:\\Users\\Ro\\PycharmProjects\\Application_FFR_finale_V1\\etude\\database\\sauvegarde\\backup_file.dump"
    DATABASE = "application_ffr_db"
    POSTGRESQL_BIN = "C:\\Program Files\\PostgreSQL\\13\\bin"



    # configuration spécifique pour Windows
    os.chdir(POSTGRESQL_BIN) # on se déplace dans le répertoire des binaires de postgresql (évite de configurer une variable d'environnement sous Windows
    os.environ["PGPASSWORD"] = PASSWORD # définit le mot de passe pour la sessions en cours, car sous Windows, le mot de passe ne peut être soumis via la ligne de commande
    print("Répertoire de travail redéfinit : " + os.getcwd())



    command = "pg_dump -U {0} -h {1} -p {2} -Fc {3} > {4}".format(USER, SERVER, PORT, DATABASE, SCRIPTS_DIRECTORY)
    print(command)
    os.system(command)


    print("Fin des traitements.")
