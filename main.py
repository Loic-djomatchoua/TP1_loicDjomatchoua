# Nom : [A REMPLACER]
# Numero etudiant : [A REMPLACER]
# GitHub : [A REMPLACER]

import argparse
import sys

from PySide6.QtWidgets import QApplication

from app.core.generator import PasswordGenerator
from app.ui.main_windows import MainWindow


def main():
    """Point d'entrée du programme : lance le mode console ou l'interface graphique."""

    parser = argparse.ArgumentParser(
        description="Générateur et coffre-fort"
    )

    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Mode ligne de commande"
    )

    parser.add_argument(
        "--vault_file",
        default="vault.json",
        help="Fichier JSON du coffre"
    )

    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Longueur du mot de passe"
    )

    for option in ("lower", "upper", "digits", "symbols"):
        parser.add_argument(
            f"--no-{option}",
            action="store_true"
        )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Exiger chaque type de caractères sélectionné"
    )

    args = parser.parse_args()

    if args.no_gui:
        return generer_en_console(args)

    return lancer_interface_graphique(args)


def generer_en_console(args):
    """Génère un mot de passe directement dans le terminal."""

    try:
        generator = PasswordGenerator(
            length=args.length,
            use_lower=not args.no_lower,
            use_upper=not args.no_upper,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            validate=args.validate
        )

        password = generator.generer()
        print(password)

    except ValueError as error:
        parser = argparse.ArgumentParser()
        parser.error(str(error))

    return 0


def lancer_interface_graphique(args):
    """Lance l'interface graphique du coffre-fort."""

    app = QApplication([sys.argv[0]])
    app.setStyle("Fusion")
    window = MainWindow(args.vault_file)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())