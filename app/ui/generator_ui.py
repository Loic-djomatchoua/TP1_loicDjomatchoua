# Nom: Loic Geoffrey Djomacthoua
# Numero d'etudiant: 2392019
# Github: TP-LoicDjomatchoua


class GeneratorFenetre(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setWindowTitle("Genereateur de mot de passe")
        self.resize(600,450)
        self.mot_recent = ""

        layout = QVBoxLayout()
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
        self.mot_label.setInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse
                                           | Qt.TextInteractionFlag.TextSelectableByKeyboard)
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
        generer.setObjectName("Marron")
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


