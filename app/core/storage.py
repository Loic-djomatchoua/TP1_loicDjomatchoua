# Nom: Loic Geoffrey Djomacthoua
#Numero etudiant: 2392019
# GitHub: Loic-djomatchoua

import json
import os


class StorageError(Exception):
 """Erreur liée au chargement ou à la sauvegarde du coffre"""

class VaultStorage:
    """Gestion du fichier JSON du coffre-fort, avec gestion d'erreurs."""

    def __init__(self, filepath="vault.json"):
        self.filepath = filepath

    def valider(self,entrees):
        if not isinstance(entrees, list):
            raise StorageError("Le coffre doit contenir une liste.")

        for entre in entrees:
            if not isinstance(entre, dict):
                raise StorageError("Une entrée du coffre est invalide")

            if "email" not in entre:
                raise StorageError("Une entrée ne contient pâs d'e-mail")
            if "mot_passe" not in entre:
                raise StorageError("Une entrée ne contient pas de mot de passe")

            if not isinstance(entre["email"],str):
                raise StorageError("L'e-mail doit être du texte")

            if not isinstance(entre["mot_passe"],str):
                raise StorageError("Le mot de passe doit être du texte")

            if entre["email"].strip() == "":
                raise StorageError("L'e-mail ne doit pas être vide")

            if entre["mot_passe"] == "":
                raise StorageError("Le mot de passe ne doit pas être vide")

    def chargement(self):
       """Charge les entrées depuis le fichier JSON"""

       try:
           with open(self.filepath, "r", encoding="utf-8") as file:
               entrees = json.load(file)

       except FileNotFoundError:
          return []

       self.valider(entrees)
       result = []

       for entre in entrees:
           nouv_entre = {
               "email": entre["email"],
               "mot_passe": entre["mot_passe"],
           }
           result.append(nouv_entre)

       return result

    def sauvegarder(self, entrees):
        """Enregistre dans les données dans le coffre"""

        self.valider(entrees)

        try:
            texte = json.dumps(entrees)

            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write(texte)

        except Exception:
            raise StorageError("Impossible d'enregistrer le fichier")

