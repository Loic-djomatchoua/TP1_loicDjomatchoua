# Noms: Loic Geoffrey Djomatchoua
# Numéro d'éudiant: 2392019
#Github: Loic-Djomatchoua

import argparse

from app.core.generator import PasswordGenerator

def parse_arguments():

    parser = argparse.ArgumentParser(
    description = "Générateur de mot de passe.")

    parser.add_argument(
        "--length",
        type = int,
        default= 16,
        help = "Longueur du mot de passe. Valeur par défaut: 16.",
    )
    parser.add_argument(
        "--no-lower",
        action = "store_true",
        help= "Exclut les lettres minuscules.",
    )
    parser.add_argument(
        "--no-upper",
        action = "store_true",
        help = "Exclut les lettres majuscules.",
    )
    parser.add_argument(
        "--no-digits",
        action = "store_true",
        help = "Exclut les chiffres",
    )
    parser.add_argument(
        "--no-symbols",
        action = "store_true",
        help = "Exclut les symboles",
    )
    parser.add_argument(
        "--validate",
        action = "store_true",
        help ="Force au moins un caractère de chaque type selectionné",
    )
    return parser.parse_args()

def main():

    arguments = parse_arguments()

    generator = PasswordGenerator(
        length=arguments.length,
        use_lower=not arguments.no_lower,
        use_upper=not arguments.no_upper,
        use_digits=not arguments.no_digits,
        use_symbols=not arguments.no_symbols,
        validate=arguments.validate,
    )

    try:
        password = generator.generer()
        print(f"Mot de passe généré: {password}")
    except ValueError as error:
        print(f"Erreur: {error}")


if __name__ == "__main__":
    main()