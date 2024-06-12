from django.db import migrations
import csv
from pathlib import Path

def import_stock(apps, schema_editor):
    csv_file_path = Path("./admin_stock/migrations/data/stock.csv")

    # Assurez-vous que le fichier CSV existe
    if not csv_file_path.is_file():
        raise FileNotFoundError(f"Le fichier {csv_file_path} est introuvable")

    with csv_file_path.open(encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Si votre fichier CSV a des en-têtes, ignorez la première ligne
        next(csv_reader, None)

        # Obtenez la référence au modèle Stock via apps.get_model
        Stock = apps.get_model('admin_stock', 'Stock')

        for row in csv_reader:
            # Ajoutez des vérifications pour vous assurer que les colonnes sont correctes
            if len(row) > 1:
                Stock.objects.get_or_create(nom_stock=row[1])
            else:
                print(f"Ligne invalide dans le fichier CSV : {row}")

class Migration(migrations.Migration):

    dependencies = [
        ('admin_stock', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_stock),
    ]
