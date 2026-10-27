import secrets
import string


class PasswordGenerator:
    def __init__(self, length=16, use_lower=True, use_upper=True,
                 use_digits=True, use_symbols=True, validate=False):
        self.length =length
        self.use_lower = use_lower
        self.use_upper = use_upper
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.validate = validate

    def generer(self):
        if type (self.length) is not int or self.length < 1:
            raise ValueError("La longueur doit être un entier strictement positif.")
        groups = [chars for enabled , chars in(
        (self.use_lower, string.ascii_lowercase),
        (self.use_upper, string.ascii_uppercase),
        (self.use_digits, string.digits),
        (self.use_symbols, string.punctuation),
        ) if enabled]
        if not groups:
            raise ValueError("Selectionnez au moins un type de caractères.")
        if self.validate and self.length < len(groups):
            raise ValueError("Longueur insuffisante pour les types selectionnés.")
        alphabet = "".join(groups)

        chars = [secrets.choice(group) for group in groups] if self.validate else []
        chars.extend(secrets.choice(alphabet)
                     for _ in range(self.length - len(chars)))
        secrets.SystemRandom().shuffle(chars)

        return "".join(chars)