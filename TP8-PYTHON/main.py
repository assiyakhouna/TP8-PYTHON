
from datetime import datetime
from contextlib import ExitStack

class ConnectionManager:

    def __init__(self, service_name):
        self.service_name = service_name

    def __enter__(self):
        print(f"[{datetime.now()}] Connexion à {self.service_name} établie.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"[{datetime.now()}] Déconnexion de {self.service_name}.")

        if exc_type:
            print(f"Erreur détectée : {exc_type.__name__} — {exc_value}")
with ConnectionManager("Serveur X") as conn:
    print(f"Travail effectué sur {conn.service_name}")

# Partie 2 : Composition avec ExitStack

with ExitStack() as stack:

    # Ouverture du fichier log
    log = stack.enter_context(open("log.txt", "a", encoding="utf-8"))

    # Connexion au serveur
    conn = stack.enter_context(ConnectionManager("Serveur X"))

    # Écriture dans le fichier log
    log.write(
        f"[{datetime.now()}] Tâche effectuée sur {conn.service_name}\n"
    )

    print("Tâche effectuée avec succès.")

# Partie 3 : Simulation d'une erreur

with ExitStack() as stack:

    log = stack.enter_context(open("log.txt", "a", encoding="utf-8"))

    conn = stack.enter_context(ConnectionManager("Base Y"))

    log.write(
        f"[{datetime.now()}] Début du traitement sur {conn.service_name}\n"
    )

    raise RuntimeError("Erreur de traitement")
