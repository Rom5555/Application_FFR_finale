# --------------------------------------------------------------------------- #
#
# script python pour la génération des tables de la base de données
# et insertion des jeux de données
#
# simplifie les modifications fréquentes nécessaire lors de la phase de
# conception, permet de rejouer fréquemment une reconstruction complète
# des éléments, en mettant à jour seulement les instruction SQL qui
# ont changées.
#
# --------------------------------------------------------------------------- #
import os

if __name__ == '__main__':

    # adapter les valeurs en rapport avec la configuration de votre environnement
    # de développement
    SERVER = "localhost"
    PORT = 5432
    USER = "dev"
    PASSWORD = "ballon"
    SCRIPTS_DIRECTORY = "C:\\Users\\romfa\\Dev\\Application_FFR_V7\\application_FFR\\etude\\database\\scripts\\"
    DATABASE = "django_FFR_db"
    POSTGRESQL_BIN = "C:\\Program Files\\PostgreSQL\\13\\bin"

    SCRIPT_00 = "00_create_tables.sql"
    SCRIPT_01 = "01_stock_insert.sql"
    SCRIPT_02 = "02_consommable_insert.sql"
    SCRIPT_03 = "03_association_stock_consommable_insert.sql"
    SCRIPT_04 = "04_equipe_insert.sql"

    scripts = []
    scripts.append(SCRIPT_00)
    scripts.append(SCRIPT_01)
    scripts.append(SCRIPT_02)
    scripts.append(SCRIPT_03)
    scripts.append(SCRIPT_04)

    # configuration spécifique pour Windows
    os.chdir(POSTGRESQL_BIN) # on se déplace dans le répertoire des binaires de postgresql (évite de configurer une variable d'environnement sous Windows
    os.environ["PGPASSWORD"] = PASSWORD # définit le mot de passe pour la sessions en cours, car sous Windows, le mot de passe ne peut être soumis via la ligne de commande
    print("Répertoire de travail redéfinit : " + os.getcwd())

    i = 0
    for script in scripts:
        print("Exécution de : '{0}'".format(script) + " ...")

        command = "psql.exe -U {0} -h {1} -p {2} -d {3} -a -f {4} > {6}".format(USER, SERVER, PORT, DATABASE, SCRIPTS_DIRECTORY + script, PASSWORD, SCRIPTS_DIRECTORY + "command_{0}.log".format(i))
        print(command)
        os.system(command)
        i = i + 1

    print("Fin des traitements.")
