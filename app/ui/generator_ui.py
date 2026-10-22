from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt

from app.core.generator import PasswordGenerator



def __init__(self):
    super().__init__(self)
    self.setWindowTitle("Générateur de mot de passe")
    self.resize(420, 380)
    self.visible = True
    self.current_password = ""
    self.init_ui()


def init_ui(self):
    layout = QVBoxLayout(self)

    # Affichage du mot de passe
    self.label_password = QLabel("")
    self.label_password.setWordWrap(True)
    self.label_password.setTextInteractionFlags(Qt.TextSelectableByMouse)
    self.label_password.setStyleSheet(
        "font-family: Consolas; font-size: 14px; "
        "background: #f0f0f0; padding: 10px; border: 1px solid #ccc;"
    )
    layout.addWidget(self.label_password)

    btn_toggle = QPushButton("👁 Afficher/Masquer")
    btn_toggle.clicked.connect(self.toggle_visibility)
    layout.addWidget(btn_toggle)

    # Longueur
    length_layout = QHBoxLayout()
    length_layout.addWidget(QLabel("Longueur :"))
    self.label_length = QLabel("16")
    self.label_length.setStyleSheet("font-weight: bold;")
    length_layout.addWidget(self.label_length)

    btn_minus = QPushButton("−")
    btn_minus.setFixedWidth(40)
    btn_minus.clicked.connect(lambda: self.adjust_length(-1))
    length_layout.addWidget(btn_minus)

    btn_plus = QPushButton("+")
    btn_plus.setFixedWidth(40)
    btn_plus.clicked.connect(lambda: self.adjust_length(1))
    length_layout.addWidget(btn_plus)
    layout.addLayout(length_layout)

    self.slider = QSlider(Qt.Horizontal)
    self.slider.setRange(4, 32)
    self.slider.setValue(16)
    self.slider.valueChanged.connect(
        lambda v: self.label_length.setText(str(v))
    )
    layout.addWidget(self.slider)

    # Types de caractères
    self.chk_lower = QCheckBox("Lettres minuscules (a-z)")
    self.chk_lower.setChecked(True)
    self.chk_upper = QCheckBox("Lettres majuscules (A-Z)")
    self.chk_upper.setChecked(True)
    self.chk_digits = QCheckBox("Chiffres (0-9)")
    self.chk_digits.setChecked(True)
    self.chk_symbols = QCheckBox("Symboles (!@#$%...)")
    layout.addWidget(self.chk_lower)
    layout.addWidget(self.chk_upper)
    layout.addWidget(self.chk_digits)
    layout.addWidget(self.chk_symbols)

    # Actions
    btn_generate = QPushButton("Générer")
    btn_generate.setStyleSheet("background: #28a745; color: white; padding: 8px;")
    btn_generate.clicked.connect(self.generate)
    layout.addWidget(btn_generate)

    btn_copy = QPushButton("Copier")
    btn_copy.setStyleSheet("background: #6c757d; color: white; padding: 8px;")
    btn_copy.clicked.connect(self.copy_password)
    layout.addWidget(btn_copy)

    self.generate()


def adjust_length(self, delta):
    new_val = self.slider.value() + delta
    if 4 <= new_val <= 32:
        self.slider.setValue(new_val)


def generate(self):
    try:
        gen = PasswordGenerator(
            length=self.slider.value(),
            use_lower=self.chk_lower.isChecked(),
            use_upper=self.chk_upper.isChecked(),
            use_digits=self.chk_digits.isChecked(),
            use_symbols=self.chk_symbols.isChecked(),
            validate=False,
        )
        self.current_password = gen.generate()
        self.display_password()
    except ValueError as e:
        QMessageBox.warning(self, "Erreur", str(e))


def display_password(self):
    if self.visible:
        self.label_password.setText(self.current_password)
    else:
        self.label_password.setText("•" * len(self.current_password))


def toggle_visibility(self):
    self.visible = not self.visible
    self.display_password()


def copy_password(self):
    if self.current_password:
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_password)
        QMessageBox.information(self, "Copié", "Mot de passe copié !")