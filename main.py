import argparse
import sys
from app.core.generator import PasswordGenerator
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    parser = argparse.ArgumentParser(description = "Générateur et coffre-fort")
    parser.add_argument("--no-gui",action = "store_true", help ="Mode ligne de commande")
    parser.add_argument("--vault_file",default= "vault.json",help="Fichier Json")
    parser.add_argument("--length", type=int, defualt=16)
    for option in ("lower", "upper", "digits", "symbols"):
        parser.add_argument(f"--no-{option}", action = "store_true")
    parser.add_argument("--validate", action = "store_true")
    args = parser.parse_args()

    if args.no_gui:
        try:
            print(PasswordGenerator(
                length=args.length, use_lower=not args.no_lower,
                use_upper=not args.no_upper, use_digits=not args.no_digits,
                use_symbols=not args.no_symbols, validate=args.validate
            ).generate())
        except ValueError as exc:
            parser.error(str(exc))
        return 0

    app = QApplication([sys.argv[0]])
    app.setStyle("Fusion")
    window = MainWindow(args.vault_file)
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())