# Nom : [Votre nom]
# Numéro d'étudiant : [Votre numéro]
# GitHub : [votre-username]

import json
import os


class VaultStorage:
    """Gestion du fichier JSON du coffre-fort, avec gestion d'erreurs."""

    def __init__(self, filepath="vault.json"):
        self.filepath = filepath

    def load(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Format invalide")
            return data
        except (json.JSONDecodeError, ValueError, OSError):
            # Fichier corrompu : on retourne une liste vide plutôt que de planter
            return []

    def save(self, entries):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise IOError(f"Impossible de sauvegarder : {e}")

    def add_entry(self, email, password):
        entries = self.load()
        entries.append({"email": email, "password": password})
        self.save(entries)

    def update_entry(self, index, email, password):
        entries = self.load()
        if 0 <= index < len(entries):
            entries[index] = {"email": email, "password": password}
            self.save(entries)

    def delete_entry(self, index):
        entries = self.load()
        if 0 <= index < len(entries):
            entries.pop(index)
            self.save(entries)