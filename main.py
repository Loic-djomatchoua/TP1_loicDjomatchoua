## Nom : [Votre nom]
# Numéro d'étudiant : [Votre numéro]
# GitHub : [votre-username]

import argparse
import sys

from app.core.generator import PasswordGenerator


def run_cli(args):
    generator = PasswordGenerator(
        length=args.length,
        use_lower=not args.no_lower,
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        validate=args.validate,
    )
    try:
        print(generator.generate())
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)


def run_ui(vault_file):
    from PySide6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow(vault_file=vault_file)
    window.show()
    sys.exit(app.exec())


def main():
    parser = argparse.ArgumentParser(description="Générateur de mots de passe et coffre-fort")
    parser.add_argument("--no-gui", action="store_true",
                        help="Exécuter en mode CLI (sans interface graphique)")
    parser.add_argument("--vault_file", type=str, default="vault.json",
                        help="Chemin du fichier JSON du coffre-fort")
    parser.add_argument("--length", type=int, default=16,
                        help="Longueur du mot de passe (défaut: 16)")
    parser.add_argument("--no-lower", action="store_true",
                        help="Exclure les minuscules")
    parser.add_argument("--no-upper", action="store_true",
                        help="Exclure les majuscules")
    parser.add_argument("--no-digits", action="store_true",
                        help="Exclure les chiffres")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclure les symboles")
    parser.add_argument("--validate", action="store_true",
                        help="Exiger au moins un caractère de chaque type actif")

    args = parser.parse_args()

    if args.no_gui:
        run_cli(args)
    else:
        run_ui(args.vault_file)


if __name__ == "__main__":
    main()