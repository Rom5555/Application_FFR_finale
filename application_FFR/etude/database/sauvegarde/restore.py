import os

if __name__ == '__main__':

    # adapter les valeurs en rapport avec la configuration de votre environnement
    # de développement
    SERVER = "localhost"
    PORT = 5432
    USER = "dev"
    PASSWORD = "ballon"
    SCRIPTS_DIRECTORY = "C:\\Users\\romfa\\Dev\\Application_FFR_V5\\database\\sauvegarde\\backup_file.dump"
    DATABASE = "application_FFR_V5_db"
    POSTGRESQL_BIN = "C:\\Program Files\\PostgreSQL\\13\\bin"


    # configuration spécifique pour Windows
    os.chdir(POSTGRESQL_BIN) # on se déplace dans le répertoire des binaires de postgresql (évite de configurer une variable d'environnement sous Windows
    os.environ["PGPASSWORD"] = PASSWORD # définit le mot de passe pour la sessions en cours, car sous Windows, le mot de passe ne peut être soumis via la ligne de commande
    print("Répertoire de travail redéfinit : " + os.getcwd())





    command = "pg_restore -U {0} -h {1} -p {2} -d {3} {5} ".format(USER, SERVER, PORT, DATABASE, PASSWORD, SCRIPTS_DIRECTORY )
    print(command)
    os.system(command)



    print("Fin des traitements.")
