# Noms: Loic Geoffrey Djomatchoua
# Numéro d'éudiant: 2392019
#Github: Loic-Djomatchoua


import random
import string

class PasswordGenerator:

    def __init__(
        self,
        length=16,
        use_lower=True,
        use_upper=True,
        use_digits=True,
        use_symbols=True,
        validate=True,
    ):
        self.length = length
        self.use_lower = use_lower
        self.use_upper = use_upper
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.validate = validate

    def generer(self):
        groupes = []

        if self.use_lower:
            groupes.append(string.ascii_lowercase)

        if self.use_upper:
            groupes.append(string.ascii_uppercase)

        if self.use_digits:
            groupes.append(string.digits)

        if self.use_symbols:
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