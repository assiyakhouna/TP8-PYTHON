
import csv
from datetime import datetime


# ==========================================
# Classe BatchProcessor
# ==========================================

class BatchProcessor:

    def __init__(self, csv_file, log_file):
        self.csv_file = csv_file
        self.log_file = log_file
        self.csv = None
        self.log = None

    # --------------------------------------
    # Ouverture des fichiers
    # --------------------------------------

    def __enter__(self):

        try:
            self.csv = open(
                self.csv_file,
                "r",
                encoding="utf-8-sig",
                newline=""
            )

            self.log = open(
                self.log_file,
                "a",
                encoding="utf-8"
            )

            self.journaliser("Début du traitement.")

            return self

        except OSError as e:

            print(f"Erreur d'ouverture : {e}")

            if self.csv:
                self.csv.close()

            if self.log:
                self.log.close()

            raise

    # --------------------------------------
    # Journalisation
    # --------------------------------------

    def journaliser(self, message):

        try:
            self.log.write(
                f"[{datetime.now()}] {message}\n"
            )
            self.log.flush()

        except OSError as e:
            print(f"Erreur d'écriture dans le journal : {e}")
            raise

    # --------------------------------------
    # Traitement des opérations CSV
    # --------------------------------------

    def traiter_operations(self):

        try:
            lecteur = csv.DictReader(self.csv)

            if not lecteur.fieldnames or "operation" not in lecteur.fieldnames:
                raise ValueError(
                    "Le fichier CSV doit contenir une colonne 'operation'."
                )

            for ligne in lecteur:

                operation = ligne["operation"]

                print(f"Traitement : {operation}")

                self.journaliser(
                    f"Opération exécutée : {operation}"
                )

        except (OSError, csv.Error, KeyError, ValueError) as e:

            self.journaliser(f"Erreur de traitement : {e}")
            raise

    # --------------------------------------
    # Fermeture des fichiers
    # --------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):

        try:
            if exc_type:
                self.journaliser(
                    f"Erreur détectée : {exc_type.__name__} - {exc_value}"
                )
            else:
                self.journaliser(
                    "Fin du traitement avec succès."
                )

        finally:

            if self.csv and not self.csv.closed:
                self.csv.close()

            if self.log and not self.log.closed:
                self.log.close()

        return False


# ==========================================
# Programme principal
# ==========================================

try:

    with BatchProcessor("operations.csv", "journal.log") as batch:
        batch.traiter_operations()

    print("\nToutes les opérations sont terminées.")

except Exception as e:

    print(f"\nUne erreur est survenue : {e}")
