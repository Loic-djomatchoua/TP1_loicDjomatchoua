
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QCheckBox, QMessageBox, QApplication
)
from PySide6.QtCore import Qt

from app.core.generator import PasswordGenerator


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Générateur de mot de passe")
        self.visible = True
        self.mot_recent = ""
        self.init_ui()

    def init_ui(self):
       layout = QVBoxLayout()
       label = QLabel("Longueur du mot de passe")
       layout.addWidget(label)

       longueur_layout = QHBoxLayout()
       btn_minus = QPushButton("-")
       btn_minus.setFixedWidth(40)
       btn_minus.clicked.connect(lambda: self.ajuster_longueur(-1))
       longueur_layout.addWidget(btn_minus)

       self.slider = QSlider(Qt.Orientation.Horizontal)
       self.slider.setRange(4,32)
       self.slider.setValue(16)
       self.slider.valueChanged.connect(
           lambda v: self.label_label_longueur.setText(str(v))
       )
       longueur_layout.addWidget(self.slider)

       btn_plus = QPushButton("+")
       btn_plus.setFixedWidth(40)
       btn_plus.clicked.connect(lambda: self.ajuster_longueur(1))
       longueur_layout.addWidget(btn_plus)

       layout.addLayout(longueur_layout)

       layout_secondaire =QHBoxLayout()
       layout_secondaire.addWidget(QLabel("9 caractères minimum"))
       self.label_longueur = QLabel("16")
       self.label_longueur.setStyleSheet("font-weight: bold;")
       layout_secondaire.addWidget(self.label_longueur)


       titre =QLabel("Types de caractères")

       self.verifie_miniscules =QCheckBox("Lettres minuscules (a-z)")
       self.verifie_miniscules.setChecked(True)
       self.verifie_majuscules = QCheckBox("Lettres majuscules (A-Z)")
       self.verifie_majuscules.setChecked(True)
       self.verifie_chiffres = QCheckBox("Chiffres (0-9)")
       self.verifie_chiffres.setChecked(True)
       self.verifie_symboles = QCheckBox("Symboles (!/$%)")
       self.verifie_symboles.setChecked(True)

       layout.addWidget(titre)
       layout.addWidget(self.verifie_miniscules)
       layout.addWidget(self.verifie_majuscules)
       layout.addWidget(self.verifie_chiffres)
       layout.addWidget(self.verifie_symboles)

       self.label_mot = QLabel("")
       self.label_mot.setWordWrap(True)
       self.label_mot.setTextInteractionFlags(
           Qt.TextInteractionFlag.TextSelectableByMouse
       )
       self.label_mot.setStyleSheet(
           "font-family: Consolas; font-size: 14px; "
           "background: #f0f0f0; padding: 10px; border: 1px solid #ccc;"
       )

       layout.addWidget(self.label_mot)


       btn_masquer = QPushButton("Afficher / Masquer")
       btn_masquer.clicked.connect(self.toggle_visibility)
       layout.addWidget(btn_masquer)


       btn_generate = QPushButton("Générer")
       btn_generate.setStyleSheet("background: #28a745; color: white; padding: 8px;")
       btn_generate.clicked.connect(self.generer)
       layout.addWidget(btn_generate)

       btn_copie = QPushButton("Copier")
       btn_copie.setStyleSheet("background: #6c757d; color: white; padding: 8px;")
       btn_copie.clicked.connect(self.copie_mot)
       layout.addWidget(btn_copie)

       # Assigner le layout à la fenêtre via un widget central
       central_widget = QWidget()
       central_widget.setLayout(layout)
       self.setCentralWidget(central_widget)

       self.generer()

    def ajuster_longueur(self, delta):
        nouvel_valeur = self.slider.value() + delta
        if 4 <= new_val <= 32:
            self.slider.setValue(nouvel_valeur)

    def generer(self):
        try:
            gen = PasswordGenerator(
                length=self.slider.value(),
                use_lower=self.verifie_minuscule.isChecked(),
                use_upper=self.verifie_majuscule.isChecked(),
                use_digits=self.verifie_chiffres.isChecked(),
                use_symbols=self.verifie_symboles.isChecked(),
                validate=False,
            )
            self.current_password = gen.generer()
            self.masque_mot()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))

    def masque_password(self):
        if self.visible:
            self.label_password.setText(self.mot_recent)
        else:
            self.label_password.setText("*" * len(self.mot_recent))

    def masque_visibilite(self):
        self.visible = not self.visible
        self.masque_mot()

    def copie_mot(self):
        if self.mot_recent:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.mot_recent)
            QMessageBox.information(self, "Copié", "Mot de passe copié dans le presse-papiers !")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(420, 400)
    window.show()
    sys.exit(app.exec())