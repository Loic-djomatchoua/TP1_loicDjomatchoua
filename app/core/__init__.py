#

import json
import os

VAULT_FILE  = "vault.json"

class VaultStorage:
    def __init__(self,filepath= VAULT_FILE):
        self.filepath = filepath

    def chargement(self):
        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath,'r',  encoding="utf-8") as json_file:
               return json.load(json_file)

    def sauvegarde(self,entries):
        with open(self.filepath,'w', encoding = "utf-8") as json_file :
         json.dump(entries,json_file,indent=4, ensure_ascii=False)

    def ajouter_entree(self, titre, nom_utilisateur,mot_de_passe):
        entries = self.chargement()
        entries.append({
            'titre': titre,
            'nom_utilisateur': nom_utilisateur,
            'mot_de_passe': mot_de_passe
        })
        self.save(entries)

    def supprimer_entree(self,index):
        entries = self.chargement()
        if 0 <= index < len(entries):
             entries.pop(index)
             self.chargement(entries)