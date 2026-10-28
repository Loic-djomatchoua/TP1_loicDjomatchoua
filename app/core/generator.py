
import secrets
import string


class PasswordGenerator:

    def __init__(self, length=16, use_lower=True, use_upper=True,
                 use_digits=True, use_symbols=True, validate=False):

        self.length = length
        self.use_lower = use_lower
        self.use_upper = use_upper
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.validate = validate

    def generer(self):

        if type(self.length) is not int:
            raise ValueError("La longueur doit être un entier.")

        if self.length < 1:
            raise ValueError("La longueur doit être supérieure à zéro.")

        groups = []

        if self.use_lower:
            groups.append(string.ascii_lowercase)

        if self.use_upper:
            groups.append(string.ascii_uppercase)

        if self.use_digits:
            groups.append(string.digits)

        if self.use_symbols:
            groups.append(string.punctuation)

        if len(groups) == 0:
            raise ValueError("Sélectionnez au moins un type de caractères.")

        if self.validate:
            if self.length < len(groups):
                raise ValueError(
                    "La longueur est insuffisante pour les types sélectionnés."
                )


        alphabet = ""

        for group in groups:
            alphabet += group


        caracteres = []

        if self.validate:
            for group in groups:
                character = secrets.choice(group)
                caracteres.append(character)


        while len(caracteres) < self.length:
            character = secrets.choice(alphabet)
            caracteres.append(character)

        random_generator = secrets.SystemRandom()
        random_generator.shuffle(caracteres)


        mot_passe = ""

        for character in caracteres:
            mot_passe += character

        return mot_passe