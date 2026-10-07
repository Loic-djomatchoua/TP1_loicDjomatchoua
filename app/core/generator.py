# Noms: Loic Geoffrey Djomatchoua
# Numéro d'éudiant: 2392019
#Github: Loic-Djomatchoua


import random
import string

class PasswordGenerator:

    def __init__(
        self,
        length=16,
       minuscules=True,
        majuscules=True,
        chiffres=True,
        symboles=True,
        validate=True,
    ):
        self.length = length
        self.minuscules= minuscules
        self.majuscules = majuscules
        self.chiffres = chiffres
        self.symboles = symboles
        self.validate = validate

    def generer(self):
        groupes = []

        if self.minuscules:
            groupes.append(string.ascii_lowercase)

        if self.majuscules:
            groupes.append(string.ascii_uppercase)

        if self.chiffres:
            groupes.append(string.digits)

        if self.symboles:
            groupes.append(string.punctuation)

        if not groupes:
            raise ValueError("Vous devez sélectionner au moins un type de caractères")

        if self.length <= 0:
            raise ValueError("La longueur doit être supérieure à zéro")

        if self.validate and self.length < len(groupes):
            raise ValueError("La longueur est trop petite pour inclure chaque type sélectionné")

        caracteres = "".join(groupes)
        password = []

        if self.validate:
            for groupe in groupes:
                password.append(random.choice(groupe))

        choix = self.length - len(password)

        for _ in range(choix):
            password.append(random.choice(caracteres))

        random.shuffle(password)

        return "".join(password)