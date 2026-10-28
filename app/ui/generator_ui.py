# Nom: Loic Geoffrey Djomacthoua
# Numero d'etudiant: 2392019
# Github: TP-LoicDjomatchoua

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QDialog, QDialogButtonBox, QHBoxLayout,
    QLabel, QMessageBox, QPushButton, QSlider, QVBoxLayout,
)
from app.core.generator import PasswordGenerator


class GeneratorFenetre(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setWindowTitle("Generateur de mot de passe")
        self.resize(600,450)
        self.mot_recent = ""

        layout = QVBoxLayout(self)
        titre = QLabel("Generateur de mots de passe")
        titre.setObjectName("titre")
        titre.setWordWrap(True)
        layout.addWidget(QLabel("Longueur du mot de passe"))

        ligne =QHBoxLayout()
        minus = QPushButton("-")
        plus = QPushButton("+")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(8,20)
        self.slider.setValue(16)
        minus.clicked.connect(lambda: self.slider.setValue(self.slider.value() - 1))
        plus.clicked.connect(lambda: self.slider.setValue(self.slider.value() + 1))
        ligne.addWidget(minus)
        ligne.addWidget(self.slider,1)
        ligne.addWidget(plus)
        layout.addLayout(ligne)

        self.longueur_label = QLabel("16 caractères  - minimun : 8")
        self.slider.valueChanged.connect(lambda n: self.longueur_label.setText(
            f"{n} caractères -minimum : 8"))
        layout.addWidget(self.longueur_label)

        layout.addWidget(QLabel("Types de caractères"))
        self.verifies = []
        for texte in ("Lettres minuscules", "Lettres majuscules", "Chiffres", "Caractères spéciaux"):
            verifie = QCheckBox(texte)
            verifie.setChecked(True)
            layout.addWidget(verifie)
            self.verifies.append(verifie)

        self.validation = QCheckBox("Exiger au moins un caractère de chaque type")
        self.validation.setChecked(True)
        layout.addWidget(self.validation)
        layout.addStretch()

        ligne = QHBoxLayout()
        ligne.addWidget(QLabel("Mot de passe"))
        ligne.addStretch()

        self.afficher = QPushButton("Afficher")
        self.afficher.setCheckable(True)
        self.afficher.toggled.connect(self.masquer_mot_passe)
        ligne.addWidget(self.afficher)
        layout.addLayout(ligne)

        self.mot_label = QLabel("Generer un mot de passe")
        self.mot_label.setObjectName("mot_passe")
        self.mot_label.setMinimumHeight(56)
        self.mot_label.setWordWrap(True)
        self.mot_label.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.mot_label)

        ligne = QHBoxLayout()
        note = QLabel("Le mot de passe est masqué par defaut.")
        note.setWordWrap(True)
        ligne.addWidget(note,1)
        self.copie_button = QPushButton("Copier")
        self.copie_button.setEnabled(False)
        self.copie_button.clicked.connect(self.copie_mot)
        ligne.addWidget(self.copie_button)
        layout.addLayout(ligne)

        generer = QPushButton("Generer un mot de passe")
        generer.setAutoDefault(False)
        generer.clicked.connect(self.generer)
        layout.addWidget(generer)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Utiliser")
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def generer(self):
        try:
            generateur = PasswordGenerator(
                length=self.slider.value(),
                use_lower=self.verifies[0].isChecked(),
                use_upper=self.verifies[1].isChecked(),
                use_digits=self.verifies[2].isChecked(),
                use_symbols=self.verifies[3].isChecked(),
                validate=self.validation.isChecked()
            )

            mot_passe = generateur.generer()


        except ValueError as erreur:

            self.erreur_label.setText(f"Erreur : {erreur}")

            self.erreur_label.show()

        else:
            self.mot_recent = mot_passe

            self.afficher.setChecked(False)
            self.masquer_mot_passe(False)

            self.copie_button.setEnabled(True)
            self.copie_button.setText("Copier")

            bouton_utiliser = self.buttons.button(
                QDialogButtonBox.StandardButton.Ok
            )
            bouton_utiliser.setEnabled(True)

    def masquer_mot_passe(self, checked):
        if self.mot_recent == "":
            self.mot_label.setText("Générez un mot de passe")

        elif checked:
            self.mot_label.setText(self.mot_recent)

        else:
            self.mot_label.setText("*" * len(self.mot_recent))

        if checked:
            self.afficher.setText("Masquer")
        else:
            self.afficher.setText("Afficher")

    def copie_mot(self):
        if self.mot_recent:
            QApplication.clipboard().setText(self.mot_recent)
            self.copie_button.setText("Copie!")

