import os
import csv
import logging

# Créer le exe :
# pyinstaller --onefile [script]

# --------------------------
# Configuration du mode debug
# --------------------------

logging.basicConfig(
    level=logging.DEBUG,
    # En fait, plusieurs niveaux :  DEBUG, INFO, WARNING, ERROR, CRITICAL ; DEBUG enregistre tout, c'est le plus complet
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", # Gabarit des lignes de log
    filename="traitement.log",
    filemode="w",
    encoding="utf-8"
)


logger = logging.getLogger(__name__)

# --------------------------
# Paramètres à modifier
# --------------------------
base_dir = input("Entrez le chemin du répertoire à traiter.\n")
lookup_csv = r".\CSV\entree.csv"
output_csv = r".\CSV\tableau.espeyran.csv"
# --------------------------

# Charger le fichier lookup dans un dictionnaire
lookup_dict = {}
with open(lookup_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter =";")
    logger.debug(f"Colonnes trouvées dans entrees.csv : {reader.fieldnames}")
    for row in reader:
        # passer de "1987" et "1" à "FRANMT_1987_1"
        if row["Serie"] == "AQ" or row["Serie"] == "AS":
            cle = f'FRANMT_{row["Sous-serie"].strip()}_{row["Serie"].strip()}'
        else:
            cle = f'FRANMT_{row["Serie"].strip()}_{row["Sous-serie"].strip()}'
        lookup_dict[cle] = row["Libelle"]

# Fonction pour compter fichiers et taille totale
def stats_recursives(path):
    total_files = 0
    total_size = 0
    extensions = set()

    for root, dirs, files in os.walk(path):
        for file in files:
            total_files += 1
            fp = os.path.join(root, file)
            total_size += os.path.getsize(fp)

            ext = os.path.splitext(file)[1].lower()
            if ext:
                extensions.add(ext)

    return total_files, total_size, sorted(list(extensions))

# Récupérer les sous-dossiers immédiats qui iront dans la colonne 1
subdirs = [
    name for name in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, name)) and name.lower() != "#recycle"
]

input("Génération du tableau pour transmission à Espeyran. Appuyez sur Entrée pour commencer.")

# Écriture du CSV de sortie
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    # quoting=csv.QUOTE_ALL permet de ne pas provoquer un saut de colonne quand il y a une virgule ;
    # tout est mis entre guillemets
    writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
    writer.writerow([
        "noms des dossiers",
        "détail",
        "nombre de dossiers",
        "nombre de fichiers",
        "poids total (Mo)",
        "extensions"
    ])

    for sub in subdirs:
        print(f"Traitement du dossier : {sub}")  # Affiche le dossier traité
        full_path = os.path.join(base_dir, sub)

        # Col. 2 : correspondance lookup
        detail = lookup_dict.get(sub, "")
        if detail == "":
            print(f"Pas de nom d'IR trouvé pour {sub}.")
        else:
            print(f"{sub} correspond à l'entrée \"{detail}.\"")

        # Col. 3 : nombre de sous-dossiers immédiats
        sub_subdirs = [
            d for d in os.listdir(full_path)
            if os.path.isdir(os.path.join(full_path, d))
        ]
        nb_sous_dossiers = len(sub_subdirs)

        # Col. 4,5,6 récursifs
        nb_files, total_bytes, extensions = stats_recursives(full_path)
        poids_mo = total_bytes / (1024 * 1024)

        writer.writerow([
            sub,
            detail,
            nb_sous_dossiers,
            nb_files,
            round(poids_mo, 2),
            ", ".join(extensions)
        ])

print("CSV généré :", output_csv)
